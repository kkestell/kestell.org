#!/usr/bin/env bash
set -e

docker build --tag=kestell .
docker run -it \
    --mount type=bind,source="$(pwd)/src",target=/k/src \
    --mount source=kestell_dist,target=/k/dist
    -h=docker --rm kestell /bin/bash
