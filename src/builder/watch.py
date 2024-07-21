import os
import threading
import time

from flask import Flask, send_from_directory
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

PORT = 8080
DIST_DIR = '/home/kyle/src/public/website/dist'
SITE_DIR = '/home/kyle/src/public/website/site'
DEBOUNCE_DELAY_SECONDS = 1

app = Flask(__name__, static_folder=DIST_DIR)


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(app.static_folder, path)


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


def start_server():
    app.run(port=PORT, use_reloader=False)


if __name__ == "__main__":
    os.system('python /home/kyle/src/public/website/src/builder/build.py')

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    event_handler = ChangeHandler('python /home/kyle/src/public/website/src/builder/build.py')
    observer = Observer()
    observer.schedule(event_handler, path=SITE_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
