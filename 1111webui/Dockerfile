FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

# region APT dependencies

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update \
    && apt-get install -y google-perftools wget git git-lfs python3 python3-venv python3-pip libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

RUN rm -f /etc/apt/apt.conf.d/proxy.conf

# endregion

# User
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

RUN test -n "$http_proxy" \
    && git config --global http.proxy $http_proxy \
    && git config --global https.proxy $https_proxy \
    || exit 0

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

ARG CUDA_VERSION="cu121"
ARG PULL_OPENAI_MODELS=""

# Main project
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git . && \
    python3 -m venv venv && \
    echo "export TORCH_COMMAND=\"pip install xformers --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/$CUDA_VERSION\"" >> "webui-user.sh" && \
    ./webui.sh --exit --skip-torch-cuda-test

# CLIP model
RUN test -n "$PULL_OPENAI_MODELS" && git clone https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14 || exit 0

# Extensions
RUN git clone --depth 1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    . ./venv/bin/activate && \
    cd extensions/sd-webui-controlnet && \
    python3 -m pip install insightface -r requirements.txt
#RUN git clone --depth 1 https://github.com/pharmapsychotic/clip-interrogator-ext.git extensions/clip-interrogator-ext
#RUN git clone --depth 1 https://github.com/zero01101/openOutpaint-webUI-extension extensions/openOutpaint-webUI-extension
#RUN git clone --depth 1 https://github.com/huchenlei/sd-webui-openpose-editor extensions/sd-webui-openpose-editor

# Install dependencies of extensions
RUN ./webui.sh --exit --skip-torch-cuda-test

RUN git config --global --unset http.proxy && \
    git config --global --unset https.proxy

CMD ["./webui.sh", "--api", "--no-download-sd-model", "--enable-insecure-extension-access", "--skip-torch-cuda-test", "--medvram", "--opt-split-attention", "--xformers", "--listen", "--port", "7860"]
