ARG UBUNTU_VERSION=22.04
ARG CUDA_VERSION=12.3.1
ARG BASE_CUDA_DEV_CONTAINER=nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}

FROM ${BASE_CUDA_DEV_CONTAINER}

WORKDIR /app

ARG CUDA_DOCKER_ARCH=all
ENV CUDA_DOCKER_ARCH=${CUDA_DOCKER_ARCH}
ENV GGML_CUDA=1

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN apt-get update \
    && apt-get install -y build-essential libsdl2-dev ffmpeg wget cmake git curl
RUN rm -f /etc/apt/apt.conf.d/proxy.conf

ENV CUDA_MAIN_VERSION=12.3
ENV LD_LIBRARY_PATH="/usr/local/cuda-${CUDA_MAIN_VERSION}/compat:$LD_LIBRARY_PATH"

RUN git clone --depth=1 "https://github.com/ggerganov/whisper.cpp.git" .
RUN make base.en

WORKDIR /tmp

ENV GO_VERSION="1.24.1"
ENV GO_ARCH="linux-amd64"

ENV GO_ZIP_URL="https://go.dev/dl/go$GO_VERSION.$GO_ARCH.tar.gz"

RUN curl -L -o go.tar.gz "$GO_ZIP_URL"  \
    && rm -rf /usr/local/go \
    && tar -C /usr/local -xzf go.tar.gz \

ENV PATH="/usr/local/go/bin:$PATH"

WORKDIR /app/bindings/go
RUN make whisper && make test

WORKDIR /app

COPY go.mod .
COPY go.sum .
RUN go mod download

COPY main.go .
RUN CGO_CFLAGS="-I/app/include -I/app/ggml/include" \
    CGO_LDFLAGS="-L/app/build_go/src -L/app/build_go/ggml/src" \
    /usr/local/go/bin/go build -o whisper main.go

EXPOSE 9090

CMD ["./whisper"]
