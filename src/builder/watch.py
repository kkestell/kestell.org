import os
import threading
import time
import argparse
from pathlib import Path

from flask import Flask, send_from_directory
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

DEBOUNCE_DELAY_SECONDS = 1


def create_app(output_dir):
    app = Flask(__name__, static_folder=output_dir)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_file(path):
        return send_from_directory(app.static_folder, path)

    return app


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, build_command):
        self.build_command = build_command
        self.last_modified = 0
        self.lock = threading.Lock()

    def on_any_event(self, event):
        if event.is_directory:
            return
        with self.lock:
            now = time.time()
            if now - self.last_modified > DEBOUNCE_DELAY_SECONDS:
                self.last_modified = now
                print(f"File changed: {event.src_path}, rebuilding...")
                os.system(self.build_command)


def start_server(app, port):
    app.run(port=port, use_reloader=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watchdog server with Flask")
    parser.add_argument("-i", "--input", default="./site/", help="Input directory path")
    parser.add_argument(
        "-o", "--output", default="./dist/", help="Output directory path"
    )
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to run the server on")
    parser.add_argument("-b", "--build-command", default="pdm run src/builder/build.py",
                        help="Build command to run on file changes")

    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()

    os.system(args.build_command)

    app = create_app(output_dir)
    server_thread = threading.Thread(target=start_server, args=(app, args.port))
    server_thread.daemon = True
    server_thread.start()

    event_handler = ChangeHandler(args.build_command)
    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
