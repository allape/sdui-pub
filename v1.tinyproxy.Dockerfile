FROM debian:stable-slim

ARG http_proxy=""
ARG https_proxy=""
ARG no_proxy=""

RUN test -n "$http_proxy" && echo "Acquire::http::Proxy \"$http_proxy\";" >> /etc/apt/apt.conf.d/proxy.conf
RUN test -n "$https_proxy" && echo "Acquire::https::Proxy \"$https_proxy\";" >> /etc/apt/apt.conf.d/proxy.conf

RUN apt-get update && apt-get install -y tinyproxy

RUN rm -Rf /etc/apt/apt.conf.d/proxy.conf

WORKDIR /root
RUN echo "#!/bin/bash" >> start.sh && \
    echo "service tinyproxy start" >> start.sh && \
    echo "tail -F /var/log/tinyproxy/tinyproxy.log" >> start.sh && \
    chmod +x start.sh

#CMD ["tinyproxy", "-d", "-c", "/etc/tinyproxy/tinyproxy.conf"]
CMD ["/root/start.sh"]
