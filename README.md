# SDUI

`StableDiffusion UI` in Docker, but now, this is a note repo for all AI-related projects.

# FAQ

- How access host network in docker container?
    - macOS and Windows: `host.docker.internal`.
    - Linux: add
      ```yaml
      extra_hosts:
        - "host.docker.internal:host-gateway"
      ```
      into a service in compose yaml file.
- How to use proxy for image building progress?
    - ```shell
        export http_proxy=http://proxy.lan:1080
        docker build \
               --build-arg "http_proxy=$http_proxy" --build-arg "https_proxy=$http_proxy"--build-arg no_proxy=localhost,127.0.0.1 \
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

- [Ollama](https://github.com/ollama/ollama)
- [open-webui](https://github.com/open-webui/open-webui)
- [Qwen](https://github.com/QwenLM/Qwen)

- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
- [GPT-SoVITS/docker-compose.yaml](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/docker-compose.yaml)

- [easyocr](https://github.com/JaidedAI/EasyOCR)

- [AudioSep](https://github.com/Audio-AGI/AudioSep)

- [ShowUI](https://github.com/showlab/ShowUI)

- [YOLO](https://github.com/ultralytics/ultralytics)

- [notification.mp3](https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/web/js/assets/notify.mp3)

- and more...

---

- [HuggingFace](https://huggingface.co/)
- [CIVITAI](https://civitai.com/)
- [Lib Lib AI](https://www.liblib.art/)
- [How does StableDiffusion work?](https://stable-diffusion-art.com/how-stable-diffusion-work/)
