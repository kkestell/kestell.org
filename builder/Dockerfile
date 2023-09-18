# Use .NET SDK image
FROM mcr.microsoft.com/devcontainers/dotnet:0-7.0 AS build-env

# Install additional dependencies
RUN apt-get update && \
    apt-get install -y pandoc texlive-xetex && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory and copy the entire builder directory
WORKDIR /site/builder
COPY . .

# Restore and publish the project
RUN dotnet restore Builder.sln
RUN dotnet publish Builder/Builder.csproj -r linux-x64 -c Release -o publish

# Set the CMD instruction to run the generator
CMD ["/site/builder/publish/builder", "build", "/site/src", "/site/dist"]
