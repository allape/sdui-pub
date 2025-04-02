package main

import (
	"fmt"
	"github.com/allape/goenv"
	"github.com/allape/gogger"
	"github.com/ggerganov/whisper.cpp/bindings/go/pkg/whisper"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
	"io"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"sync"
	"syscall"
)

type Syllable struct {
	Start uint64 `json:"start"` // ms
	End   uint64 `json:"end"`   // ms
	Text  string `json:"text"`
}

const (
	whisperModelPath = "WHISPER_MODEL_PATH"
	whisperAddr      = "WHISPER_ADDR"
	whisperCors      = "WHISPER_CORS"
)

// models/ggml-tiny.en.bin
// models/ggml-tiny.bin
// models/ggml-base.en.bin
// models/ggml-base.bin
// models/ggml-small.en.bin
// models/ggml-small.bin
// models/ggml-medium.en.bin
// models/ggml-medium.bin
// models/ggml-large-v1.bin
// models/ggml-large-v2.bin
// models/ggml-large-v3.bin
// models/ggml-large-v3-turbo.bin
var (
	ModelPath = goenv.Getenv(whisperModelPath, "models/ggml-medium.bin")
	Addr      = goenv.Getenv(whisperAddr, ":9090")
	Cors      = goenv.Getenv(whisperCors, false)
)

var l = gogger.New("main")

func main() {
	err := gogger.InitFromEnv()

	model, err := whisper.New(ModelPath)
	if err != nil {
		l.Error().Fatalf("failed to load model: %v", err)
	}
	defer func() {
		err = model.Close()
		if err != nil {
			l.Error().Printf("failed to close model: %v", err)
		}
	}()

	engine := gin.Default()

	if Cors {
		engine.Use(cors.Default())
		l.Warn().Printf("CORS enabled")
	}

	locker := sync.Mutex{}
	engine.PUT("/:language/*filename", func(context *gin.Context) {
		locker.Lock()
		defer locker.Unlock()

		modelContext, err := model.NewContext()
		if err != nil {
			l.Error().Printf("failed to create model context: %v", err)
			context.String(http.StatusInternalServerError, "model context error")
			return
		}
		//modelContext.SetMaxSegmentLength(1)

		language := context.Param("language")

		err = modelContext.SetLanguage(language)
		if err != nil {
			l.Error().Printf("failed to set language: %v", err)
			context.String(http.StatusInternalServerError, "language error")
			return
		}

		tmp, err := os.CreateTemp(os.TempDir(), "whisper-*.wav")
		if err != nil {
			l.Error().Printf("failed to create temp file: %v", err)
			context.String(http.StatusInternalServerError, "temp file error")
			return
		}
		defer func() {
			err = os.Remove(tmp.Name())
			if err != nil {
				l.Error().Printf("failed to remove temp file: %v", err)
			}
		}()

		cmd := exec.Command(
			"ffmpeg",
			"-hide_banner",
			"-y",
			"-i", "-",
			"-ar", "16000",
			"-ac", "1",
			"-c:a", "pcm_s16le",
			tmp.Name(),
		)
		cmd.Stdin = context.Request.Body

		output, err := cmd.CombinedOutput()
		l.Debug().Printf("ffmpeg output: %s", output)
		if err != nil {
			l.Error().Printf("failed to run ffmpeg: %v", err)
			context.String(http.StatusInternalServerError, "ffmpeg error")
			return
		}

		dec := wav.NewDecoder(tmp)
		if err != nil {
			l.Error().Printf("failed to decode wav: %v", err)
			context.String(http.StatusInternalServerError, "wav error")
			return
		}

		if !dec.IsValidFile() {
			l.Error().Printf("invalid wav file")
			context.String(http.StatusInternalServerError, "wav error")
			return
		}

		format := &audio.Format{
			NumChannels: int(dec.NumChans),
			SampleRate:  int(dec.SampleRate),
		}

		var samples []float32
		bufferSize := 4096
		buf := &audio.IntBuffer{Data: make([]int, bufferSize), Format: format}
		var n int
		for err == nil {
			n, err = dec.PCMBuffer(buf)
			if err != nil {
				break
			}
			if n == 0 {
				break
			}
			if n != len(buf.Data) {
				buf.Data = buf.Data[:n]
			}
			samples = append(samples, buf.AsFloat32Buffer().Data...)
		}

		if err := modelContext.Process(samples, nil, nil, nil); err != nil {
			l.Error().Printf("failed to process samples: %v", err)
			context.String(http.StatusInternalServerError, "process error")
			return
		}

		var syllables []Syllable
		for {
			segment, err := modelContext.NextSegment()
			if err != nil {
				if err != io.EOF {
					l.Error().Printf("failed to get next segment: %v", err)
					context.String(http.StatusInternalServerError, "segment error")
					return
				} else {
					break
				}
			}
			fmt.Printf("[%6s->%6s] %s\n", segment.Start, segment.End, segment.Text)
			syllables = append(syllables, Syllable{
				Start: uint64(segment.Start.Milliseconds()),
				End:   uint64(segment.End.Milliseconds()),
				Text:  segment.Text,
			})
		}

		context.JSON(http.StatusOK, syllables)
	})

	go func() {
		err = engine.Run(Addr)
		if err != nil {
			l.Error().Fatalf("failed to start server: %v", err)
		}
	}()

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	l.Info().Println("exiting with", <-sigs)
}
