FROM alpine

RUN apk update && apk add tinyproxy

RUN mkdir -p /run/tinyproxy

CMD ["tinyproxy", "-d", "-c", "/etc/tinyproxy/tinyproxy.conf"]
