#!/usr/bin/env bash

export docker_http_proxy=http://host.docker.internal:1080
export docker_image_architecture=${1:-amd64}
export docker_image_name=allape/yolo:ultralytics-8.3.75-$docker_image_architecture

docker build --platform "linux/$docker_image_architecture" --build-arg http_proxy=$docker_http_proxy --build-arg https_proxy=$docker_http_proxy -f "predictor.$docker_image_architecture.Dockerfile" -t "$docker_image_name" .

echo "Run Command"
echo "docker run -d -p 8080:8080 --network none --name yolo $docker_image_name"
