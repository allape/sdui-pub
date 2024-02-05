# SDUI

StableDiffusion UI in Docker

---

[中文](./README.cn.md) | [English](./README.md)

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

## Windows prelude

```shell
# Run this command before everything if you are using Windows
git config --global core.autocrlf false
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
git clone https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14
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

# You can ignore below commands if you have no will to mount `models` folder,
#   because we need a fresh models folder to run properly.
cd ..
git clone https://github.com/lllyasviel/Fooocus.git
cp -R Fooocus/models sdui/fooocus/
cd sdui

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

## [Ollama](https://github.com/ollama/ollama)

```shell
docker compose -f compose.ollama.yaml up -d
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
      # Backup AUTOMATIC1111/stable-diffusion-webui
      docker commit 1111webui-app-1 1111webui:v1
      # Backup ComfyUI
      docker commit comfyui-app-1 comfyui:v1
      # Backup Fooocus
      docker commit fooocus-app-1 fooocus:v1
      # Backup Ollama
      docker commit ollama-app-1 ollama/ollama:latest
      ```

# Credits

- [Docker](https://www.docker.com/)
- [ComfyUI Dockerfile](https://huggingface.co/spaces/SpacesExamples/ComfyUI/tree/main)
- [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Fooocus](https://github.com/lllyasviel/Fooocus)
- [Ollama](https://github.com/ollama/ollama)
- [tinyproxy](https://github.com/tinyproxy/tinyproxy)
- [Caddy](https://github.com/caddyserver/caddy)
- [notification.mp3](https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/web/js/assets/notify.mp3)

---

- [How does StableDiffusion work?](https://stable-diffusion-art.com/how-stable-diffusion-work/)
