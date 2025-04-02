## [whisper.cpp](https://github.com/ggerganov/whisper.cpp)

```shell
docker build --build-arg "http_proxy=$http_proxy" --build-arg "https_proxy=$https_proxy" --build-arg "no_proxy=localhost,127.0.0.1" -t allape/whisper:latest .
docker run --rm -v "$(pwd)/models:/models" -e "http_proxy=$http_proxy" allape/whisper:latest bash -c "/app/models/download-ggml-model.sh medium /models"
docker compose up -d

# docker run --gpus all -d --name whisper -p 9090:9090 -v "$(pwd)/models:/models" allape/whisper:latest bash -c "tail -F /dev/void"
```
