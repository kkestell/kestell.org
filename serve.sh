#!/usr/bin/env bash

docker run -p 1313:1313 -v $(pwd)/builder:/app/builder -v $(pwd)/src:/site/src -v $(pwd)/dist:/site/dist kestell-dot-org /site/builder/publish/builder serve /site/src /site/dist
