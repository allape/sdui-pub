FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

ARG http_proxy
ARG https_proxy
ARG no_proxy

ARG USE_PERSISTENT_DATA
ARG CUDA_VERSION=cu121
ARG PULL_OPENAI_MODELS

# region APT dependencies

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" >> /etc/apt/apt.conf.d/proxy.conf

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

RUN git config --global http.proxy $http_proxy && \
    git config --global https.proxy $https_proxy

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git . && \
    python3 -m venv venv && \
    echo "export TORCH_COMMAND=\"pip install xformers --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/$CUDA_VERSION\"" >> "webui-user.sh" && \
    ./webui.sh --exit --skip-torch-cuda-test

#RUN test -n "$PULL_OPENAI_MODELS" && git clone https://huggingface.co/openai/clip-vit-large-patch14 openai/clip-vit-large-patch14
RUN git clone --depth 1 https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet && \
    . ./venv/bin/activate && \
    cd extensions/sd-webui-controlnet && \
    python3 -m pip install insightface -r requirements.txt

RUN git config --global --unset http.proxy && \
    git config --global --unset https.proxy

CMD ["./webui.sh", "--no-download-sd-model", "--enable-insecure-extension-access", "--skip-torch-cuda-test", "--xformers", "--listen", "--port", "7860"]
