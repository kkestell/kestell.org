#!/bin/bash
for file in debian-install-*.png; do
  optipng "$file"
done
