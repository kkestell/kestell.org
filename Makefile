.PHONY: venv build serve watch

VENV_DIR := .venv
VENV_ACTIVATE := $(VENV_DIR)/bin/activate

venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		python -m venv $(VENV_DIR); \
		. $(VENV_ACTIVATE) && pip install -r requirements.txt; \
	fi

build: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. $(VENV_ACTIVATE) && python main.py; \
	else \
		python main.py -f; \
	fi

serve: venv
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. $(VENV_ACTIVATE) && python -m http.server --directory dist & \
	else \
		python -m http.server --directory dist & \
	fi

watch: venv
	@make build
	@echo "Starting server..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		. $(VENV_ACTIVATE) && python -m http.server --directory dist & echo $$! > /tmp/server.pid; \
	else \
		python -m http.server --directory dist & echo $$! > /tmp/server.pid; \
	fi
	@echo "Watching for changes. Press [CTRL+C] to stop."
	@trap 'kill $$(cat /tmp/server.pid); rm /tmp/server.pid; exit 0' SIGINT; \
	while inotifywait -r -e modify,create,delete,move src; do \
		make build; \
	done
