FROM continuumio/anaconda3:main

ENV CKPT_URL="https://huggingface.co/spaces/Audio-AGI/AudioSep/resolve/main/checkpoint/audiosep_base_4M_steps.ckpt?download=true"
ENV PT_URL="https://huggingface.co/spaces/Audio-AGI/AudioSep/resolve/main/checkpoint/music_speech_audioset_epoch_15_esc_89.98.pt?download=true"

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles

RUN apt-get update && apt-get install -y git curl build-essentials

WORKDIR /app

RUN git clone --depth=1 https://github.com/Audio-AGI/AudioSep.git . \
    && conda env create -f environment.yml \
    && conda activate AudioSep \
RUN mkdir -p checkpoint && cd checkpoint \
    && curl -Lv -O "$CKPT_URL" \
    && curl -Lv -O "$PT_URL"

COPY inference.py .
