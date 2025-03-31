FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

# region APT dependencies
#RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
#RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update \
    && apt-get install -y wget git git-lfs python3 python3-venv python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

#RUN rm -f /etc/apt/apt.conf.d/proxy.conf
# endregion

# region User
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
# endregion

WORKDIR $HOME/app

RUN test -n "$http_proxy" && git config --global http.proxy $http_proxy || exit 0
RUN test -n "$https_proxy" && git config --global https.proxy $https_proxy || exit 0

RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

RUN git clone https://github.com/showlab/ShowUI.git .
RUN python3 -m pip install -r requirements.txt

RUN git config --global --unset http.proxy && \
    git config --global --unset https.proxy

EXPOSE 7860

CMD ["python3", "app.py"]
