# See https://github.com/JaidedAI/EasyOCR/blob/master/Dockerfile

FROM docker.io/pytorch/pytorch

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" || exit 0 >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists

WORKDIR /app

#RUN test -n "$http_proxy" \
#    && git config --global http.proxy $http_proxy \
#    && git config --global https.proxy $https_proxy \
#    || exit 0

#RUN git clone "https://github.com/JaidedAI/EasyOCR.git" . \
#    && python setup.py build_ext --inplace -j 4 \
#    && python -m pip install -e .

#RUN git config --global --unset http.proxy && \
#    git config --global --unset https.proxy

RUN python -m pip install \
    pandas \
    "opencv-python-headless<4.3" \
    Pillow \
    gradio \
    torch \
    easyocr

COPY easyocr/app.py .

CMD ["python", "app.py"]
