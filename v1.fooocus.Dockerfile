FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update && \
    apt-get install -y cmake make build-essential llvm wget curl git git-lfs ffmpeg \
            python3 python3-venv python3-pip libgl1 libglib2.0-0
RUN git lfs install

RUN rm -f /etc/apt/apt.conf.d/proxy.conf

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

# Main project
RUN git clone https://github.com/lllyasviel/Fooocus.git . && \
    python3 -m pip install -r requirements_versions.txt


RUN git config --global --unset http.proxy && \
    git config --global --unset https.proxy

CMD ["python3", "entry_with_update.py", "--listen", "--output-path", "/data"]
