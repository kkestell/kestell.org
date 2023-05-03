#!/usr/bin/env bash
cd builder
dotnet publish -r linux-x64 -c Release -o publish
mkdir -p ~/.local/bin
cp publish/builder ~/.local/bin/
cd ..

