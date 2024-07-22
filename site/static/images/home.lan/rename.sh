#!/bin/bash
counter=1
find . -maxdepth 1 -name "*.png" -print0 | sort -z | while IFS= read -r -d '' file; do
  mv "$file" "debian-install-$counter.png"
  counter=$((counter + 1))
done
