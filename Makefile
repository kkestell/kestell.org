.PHONY: all build install uninstall clean check help

# Default installation prefix
PREFIX := ~/.local
BINDIR := $(PREFIX)/bin

# Default target
all: build

# Check for required commands
check:
	@command -v dotnet >/dev/null 2>&1 || { echo >&2 "dotnet is not installed. Aborting."; exit 1; }
	@command -v pandoc >/dev/null 2>&1 || { echo >&2 "pandoc is not installed. Aborting."; exit 1; }

# Build the project
build: check
	cd builder && dotnet build

# Publish and install the project
install: build
	cd builder && \
	dotnet publish -r linux-x64 -c Release -o publish && \
	mkdir -p $(BINDIR) && \
	cp publish/builder $(BINDIR)/

# Uninstall the project
uninstall:
	rm -f $(BINDIR)/builder

# Clean up build artifacts
clean:
	cd builder && \
	rm -rf bin obj publish

# Display help
help:
	@echo "Usage: make [target]"
	@echo "Available targets:"
	@echo "  all       - Build the project (default target)"
	@echo "  build     - Build the project"
	@echo "  install   - Install the project to BINDIR under PREFIX"
	@echo "  uninstall - Remove installed files from BINDIR"
	@echo "  clean     - Clean up build artifacts"
	@echo "  check     - Check for required commands"
	@echo "  help      - Display this help"
	@echo "Customization Variables:"
	@echo "  PREFIX    - Set the installation root directory (default: ~/.local)"
	@echo "              Example: make install PREFIX=/usr/local"
	@echo "  BINDIR    - Set the binary installation directory (default: \$(PREFIX)/bin)"
	@echo "              Example: make install BINDIR=/usr/bin"
	@echo "Note: BINDIR is relative to PREFIX unless an absolute path is given."
