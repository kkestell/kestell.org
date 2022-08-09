#!/usr/bin/env bash
podman run --rm -it \
  -v $(pwd):/src \
  -p 1313:1313 \
  docker.io/klakegg/hugo:0.101.0 \
  server
