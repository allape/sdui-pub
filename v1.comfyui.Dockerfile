FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update \
    && apt-get install -y make build-essential libssl-dev zlib1g-dev \
        libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
        libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git git-lfs \
        ffmpeg libsm6 libxext6 cmake libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

RUN rm -f /etc/apt/apt.conf.d/proxy.conf

# User
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

RUN git config --global http.proxy $http_proxy && \
    git config --global https.proxy $https_proxy

# Pyenv
RUN curl https://pyenv.run | bash
ENV PATH=$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH

ARG PYTHON_VERSION=3.10.12

# Python
RUN pyenv install $PYTHON_VERSION && \
    pyenv global $PYTHON_VERSION && \
    pyenv rehash && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir datasets huggingface-hub "protobuf<4" "click<8.1"

# Set the working directory to /data if USE_PERSISTENT_DATA is set, otherwise set to $HOME/app
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user

RUN git clone https://github.com/comfyanonymous/ComfyUI . && \
    pip install xformers --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu121

# Instal custom nodes
RUN echo "Installing custom nodes..."
RUN cd custom_nodes && git clone https://github.com/Fannovel16/comfy_controlnet_preprocessors && cd comfy_controlnet_preprocessors && python install.py --no_download_ckpts
RUN cd custom_nodes && git clone https://github.com/Fannovel16/comfyui_controlnet_aux && cd comfyui_controlnet_aux && pip install -r requirements.txt
RUN cd custom_nodes && git clone https://github.com/Stability-AI/stability-ComfyUI-nodes && cd stability-ComfyUI-nodes && pip install -r requirements.txt
RUN cd custom_nodes && git clone https://github.com/EllangoK/ComfyUI-post-processing-nodes
RUN cd custom_nodes && git clone https://github.com/pythongosssss/ComfyUI-Custom-Scripts
RUN echo "Done"

RUN git config --global --unset http.proxy && \
    git config --global --unset https.proxy

CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "7860", "--output-directory", "/data"]
