.PHONY: build serve watch

build:
	python main.py

serve:
	python -m http.server --directory dist &

watch:
	@echo "Starting server..."
	@python -m http.server --directory dist & echo $$! > /tmp/server.pid
	@echo "Watching for changes. Press [CTRL+C] to stop."
	@trap 'kill $$(cat /tmp/server.pid); rm /tmp/server.pid; exit 0' SIGINT; \
	while inotifywait -r -e modify,create,delete,move src; do \
		make build; \
	done
