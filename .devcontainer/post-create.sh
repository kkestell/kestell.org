#!/usr/bin/env bash
sudo apt update && sudo apt install -y fswatch
source ./venv/bin/activate
pip install -r requirements.txt