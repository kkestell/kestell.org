# Use the specified image as the base
FROM mcr.microsoft.com/devcontainers/dotnet:0-7.0

# Install Pandoc
RUN apt-get update && \
    apt-get install -y pandoc

# Install TeX Live with XeLaTeX
RUN apt-get install -y texlive-xetex

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
