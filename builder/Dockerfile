# Use Arch Linux base image
FROM archlinux:base

# Update and install dependencies
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm dotnet-sdk pandoc texlive-core pngcrush jpegoptim && \
    pacman -Scc --noconfirm

# Set working directory and copy the entire builder directory
WORKDIR /site/builder
COPY . .

# Restore and publish the project
RUN dotnet restore Builder.sln
RUN dotnet publish Builder/Builder.csproj -r linux-x64 -c Release -o publish

# Set the CMD instruction to run the generator
CMD ["/site/builder/publish/builder", "build", "/site/src", "/site/dist"]
