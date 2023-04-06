#!/usr/bin/env bash
fswatch -0 content -v | while read -d "" event
    do
        echo "File changed: $event"
        ./build.sh
    done