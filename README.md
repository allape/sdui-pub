# SDUI

StableDiffusion UI in Docker

---

[中文](./README.cn.md) | [English]

# Drivers and Tools

- [Docker](https://www.docker.com/)
- [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads)
- [WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
- [Download Git](https://git-scm.com/downloads)

# My Poor Gears

- Intel Core i7-8700K
- NVIDIA GeForce GTX 1060 6GB
- NVIDIA GeForce RTX 4070 SUPER
- 32GB DDR4 3200MHz

# Let's get started

## Prelude

```shell
# Run this command before everything if you are using Windows
#git config --global core.autocrlf false

# Output folder
mkdir data
# `Fooocus` models and configs
mkdir fooocus
# `GPT-SoVITS` models and configs
mkdir gpt-sovits
# `Ollama` models and configs
mkdir ollama
# `OpenAI` `CLIP`
mkdir openai

# `Model` / `Checkpoint` folder
mkdir -p models/checkpoints
# `LoRA` folder
mkdir -p models/loras
# `embeddings` / `Textual Inversion` folder
mkdir -p models/embeddings
# `VAE` folder
mkdir -p models/vae
mkdir -p models/vae_approx

# `Qwen` checkpoints
mkdir -p models/qwen
```

## [tinyproxy](https://github.com/tinyproxy/tinyproxy)

```shell
# tinyproxy can NOT handle `\r` in config file,
# run next command in Git Bash to parse config file on Windows
#dos2unix tinyproxy.conf

docker build -t tinyproxy:latest -f v1.tinyproxy.Dockerfile .
```

## [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

```shell
docker build -t 1111webui:v1 -f v1.1111webui.Dockerfile .

# CLIP models
git clone --depth 1 https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14
# Suggested ControlNET models
git clone --depth 1 https://huggingface.co/lllyasviel/ControlNet-v1-1 models/controlnet/ControlNet-v1-1
# FaceID IP-Adapter models
git clone --depth 1 https://huggingface.co/h94/IP-Adapter-FaceID models/controlnet/IP-Adapter-FaceID

docker compose -f compose.1111webui.yaml up -d
```

## [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

```shell
docker build -t comfyui:v1 -f v1.comfyui.Dockerfile .
docker compose -f compose.comfyui.yaml up -d
```

## [Fooocus](https://github.com/lllyasviel/Fooocus)

```shell
docker build -t fooocus:v1 -f v1.fooocus.Dockerfile .

# Get required files
# Method 1
#cd ..
#git clone --depth 1 https://github.com/lllyasviel/Fooocus.git
#cp -R Fooocus/models sdui/fooocus/
#cd sdui
# Method 2
export TMP_FOOOCUS_CONTAINER="$(docker create fooocus:v1)"
docker cp "$TMP_FOOOCUS_CONTAINER:/home/user/app/models" fooocus/
docker rm -f "$TMP_FOOOCUS_CONTAINER"

# --preset anime
#export FOOOCUS_PRESET="anime"
# --preset realistic
#export FOOOCUS_PRESET="realistic"
# --preset lcm
#export FOOOCUS_PRESET="lcm"
# --preset sai
#export FOOOCUS_PRESET="sai"

# --preset default
export FOOOCUS_PRESET="default"
docker compose -f compose.fooocus.yaml up -d
```

## [Qwen](https://github.com/QwenLM/Qwen)

```shell
git clone --depth 1 https://huggingface.co/Qwen/Qwen-7B-Chat ./models/qwen
docker compose -f compose.qwen.yaml up -d
```

## [Ollama](https://github.com/ollama/ollama)

```shell
docker compose -f compose.ollama.yaml up -d
```

## [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)

```shell
git clone --depth 1 https://huggingface.co/lj1995/GPT-SoVITS ./gpt-sovits/SoVITS_weights
docker compose -f compose.gpt-sovits.yaml up -d
```

# FAQ

- How to use proxy for image building progress?
    - ```shell
        export proxy_host=proxy.lan:1080
        docker build \
               --build-arg "http_proxy=http://$proxy_host" \
               --build-arg "https_proxy=http://$proxy_host" \
               --build-arg no_proxy=localhost,127.0.0.1 \
               --progress=plain \
               -t image:tag -f Dockerfile .
      ```
- Failed to install NVIDIA CUDA driver
    - Find out the modules that were failed to install on the Installation Summary Dialog
    - Then rerun the installer, and uncheck the modules that were failed to install.
      And at the same time, download the modules from NVIDIA developer website and install them manually.
    - For me, I failed to install `nsight-compute`. After all above steps, Everything works fine.
- How backup container?
    - ```shell
      docker commit 1111webui-app-1 1111webui:v1
      ```
- How backup image?
    - ```shell
      docker image save 1111webui:v1 -o 1111webui.v1.tar
      ```

# Credits

- [Docker](https://www.docker.com/)
- [Caddy](https://github.com/caddyserver/caddy)
- [tinyproxy](https://github.com/tinyproxy/tinyproxy)
- [dufs](https://github.com/sigoden/dufs)

- [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [ComfyUI Dockerfile](https://huggingface.co/spaces/SpacesExamples/ComfyUI/tree/main)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [MAT](https://huggingface.co/spaces/Rothfeld/stable-diffusion-mat-outpainting-primer/tree/main)
- [Fooocus](https://github.com/lllyasviel/Fooocus)

- [Ollama](https://github.com/ollama/ollama)
- [open-webui](https://github.com/open-webui/open-webui)
- [Qwen](https://github.com/QwenLM/Qwen)

- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- [GPT-SoVITS/docker-compose.yaml](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/docker-compose.yaml)

- [notification.mp3](https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/web/js/assets/notify.mp3)

- and more...

---

- [HuggingFace](https://huggingface.co/)
- [CIVITAI](https://civitai.com/)
- [Lib Lib AI](https://www.liblib.art/)
- [How does StableDiffusion work?](https://stable-diffusion-art.com/how-stable-diffusion-work/)
