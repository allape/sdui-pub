# SDUI

在 Docker 中部署 StableDiffusion UI 工程

---

[English](./README.md) | [中文]

# 需要下载的驱动和工具

- [Docker](https://www.docker.com/)
- [NVIDIA CUDA](https://developer.nvidia.com/cuda-downloads)
- [WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
- [Download Git](https://git-scm.com/downloads)

# 我的装备

- Intel Core i7-8700K
- NVIDIA GeForce GTX 1060 6GB
- NVIDIA GeForce RTX 4070 SUPER
- 32GB DDR4 3200MHz

# 如何开始

## 在 Windows 上要干的事儿

```shell
git config --global core.autocrlf false
```

## 构建一个 [tinyproxy](https://github.com/tinyproxy/tinyproxy) 镜像

因为使用 Docker 就是希望隔离 UI 项目, 避免其直接访问到互联网, 或被其污染主机环境

```shell
# 如果是在 Windows 中运行, 需要先在 Git Bash 中执行以下以下语句
#dos2unix tinyproxy.conf

docker build -t tinyproxy:latest -f v1.tinyproxy.Dockerfile .
```

### 测试 [tinyproxy](https://github.com/tinyproxy/tinyproxy) 代理服务器是否正常工作

如果需要上游代理的, 将 [tinyproxy.conf](tinyproxy.conf) 的最后一行, 取消注释, 并替换成你自己的代理地址即可;
不需要上游代理的, 可以将下面的 [duckduckgo.com](https://duckduckgo.com) 替换成其他网站

```shell
#docker exec -it tinyproxy bash
unset http_proxy
docker rm -f tinyproxy
docker run -d -p 8119:8118 --name tinyproxy -v "$(pwd)/tinyproxy.conf:/etc/tinyproxy/tinyproxy.conf" tinyproxy:latest
curl -v duckduckgo.com
export http_proxy=http://127.0.0.1:8119
curl -v duckduckgo.com
docker rm -f tinyproxy
```

## [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

这是一个很好用、很出名的 SD UI 工程

```shell
# 构建镜像
docker build -t 1111webui:v1 -f v1.1111webui.Dockerfile .

# 拉取分词+图文模型
git clone https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14
# 推荐使用的 ControlNET 模型
git clone https://huggingface.co/lllyasviel/ControlNet-v1-1 models/controlnet/ControlNet-v1-1
# FaceID IP-Adapter 模型
git clone https://huggingface.co/h94/IP-Adapter-FaceID models/controlnet/IP-Adapter-FaceID

docker compose -f compose.1111webui.yaml up -d
```

## [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

这是一个基于图形化节点编程的 SD UI 工程

```shell
# 构建镜像
docker build -t comfyui:v1 -f v1.comfyui.Dockerfile .
# 启动容器
docker compose -f compose.comfyui.yaml up -d
```

## [Fooocus](https://github.com/lllyasviel/Fooocus)

这是一个极简的 SDUI 项目, 要比 [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 简单很多;
但是, 与此同时, 也失去了很多自定义的功能

```shell
docker build -t fooocus:v1 -f v1.fooocus.Dockerfile .

# 获取最新的数据
# 方法 1
#cd ..
#git clone https://github.com/lllyasviel/Fooocus.git
#cp -R Fooocus/models sdui/fooocus/
#cd sdui
# 方法 2
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

阿里巴巴的 `通义千问`

```shell
docker compose -f compose.qwen.yaml up -d
```

## [Ollama](https://github.com/ollama/ollama)

这不是一个 SD 的工程, 但是可以用来跑大语言模型, 正好 SDUI 的基础设施可以直接搭建构建这个镜像

```shell
docker compose -f compose.ollama.yaml up -d
```

# 常见问题

- 如何在构建镜像过程中使用上游代理服务?
    - 参考构建 tinyproxy 的过程, 在构建镜像时, 传入 `--build-arg` 参数即可
    - ```shell
      export proxy_host=proxy.lan:1080
      docker build \
             --build-arg "http_proxy=http://$proxy_host" \
             --build-arg "https_proxy=http://$proxy_host" \
             --build-arg no_proxy=localhost,127.0.0.1 \
             --progress=plain \
             -t image:tag -f Dockerfile .
    ```
- 英伟达 CUDA 驱动安装失败
    - 可能因为我的显卡比较老了, 安装 CUDA 的时候提示 nsight compute 什么什么的安装失败了.
      所以在安装 CUDA 的时候, 选择自定义安装, 然后取消勾选 nsight compute, 先把 CUDA 其他模块安装完成.
      然后再去英伟达官网下载 nsight compute 相关的安装包, 一顿安装, 就可以了.
    - 因为我也不确定有没有 nsight compute 会不会对 pytorch 有影响, 反正现在能正常跑起来了.
    - 出现类似问题的小伙伴也可以通过在`安装错误的结果页面`找到对应出错的模块, 按照上面的思路进行就好了.
- 如何备份 Docker 容器? (因为更改配置之后重启 compose 会丢失原有容器内容)
    - ```shell
      # 备份 `AUTOMATIC1111/stable-diffusion-webui`
      docker commit 1111webui-app-1 1111webui:v1
      ```
- 如何备份 Docker 镜像?
    - ```shell
      # 导出 `AUTOMATIC1111/stable-diffusion-webui` 为 `1111webui.v1.tar`
      docker image save 1111webui:v1 -o 1111webui.v1.tar
      # 然后将 `1111webui.v1.tar` 放到安全的地方
      ```

# 词汇表

- SD: Stable Diffusion
- UI: User interface

# 感谢名单以及代码来源(Credits)

- [Docker](https://www.docker.com/)
- [Caddy](https://github.com/caddyserver/caddy)
- [tinyproxy](https://github.com/tinyproxy/tinyproxy)

- [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [ComfyUI Dockerfile](https://huggingface.co/spaces/SpacesExamples/ComfyUI/tree/main)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [MAT](https://huggingface.co/spaces/Rothfeld/stable-diffusion-mat-outpainting-primer/tree/main)
- [Fooocus](https://github.com/lllyasviel/Fooocus)

- [Ollama](https://github.com/ollama/ollama)
- [Qwen](https://github.com/QwenLM/Qwen)

- [notification.mp3](https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/web/js/assets/notify.mp3)

- 其他更多爱心人士...

---

- [HuggingFace](https://huggingface.co/)
- [CIVITAI](https://civitai.com/)
- [Lib Lib AI](https://www.liblib.art/)
- [How does StableDiffusion work?](https://stable-diffusion-art.com/how-stable-diffusion-work/)
