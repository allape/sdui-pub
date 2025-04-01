## [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

```shell
mkdir -p models/checkpoints
mkdir -p models/loras
mkdir -p models/embeddings
mkdir -p models/vae
mkdir -p models/vae_approx
mkdir -p openai

docker build -t allape/1111webui:latest .

# CLIP models
git clone --depth 1 https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14
# Suggested ControlNET models
git clone --depth 1 https://huggingface.co/lllyasviel/ControlNet-v1-1 models/controlnet/ControlNet-v1-1
# FaceID IP-Adapter models
git clone --depth 1 https://huggingface.co/h94/IP-Adapter-FaceID models/controlnet/IP-Adapter-FaceID

docker compose up -d
```
