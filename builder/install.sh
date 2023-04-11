#!/usr/bin/env bash
dotnet publish -r linux-x64 -c Release -o publish
cp publish/builder ~/.local/bin/
