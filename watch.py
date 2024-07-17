from flask import Flask, send_from_directory
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import signal
import time
import threading

PORT = 8080
DIRECTORY = 'dist'
SRC_DIR = 'src'
DEBOUNCE_DELAY = 1  # seconds

app = Flask(__name__, static_folder=DIRECTORY)

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
            if now - self.last_modified > DEBOUNCE_DELAY:
                self.last_modified = now
                print(f"File changed: {event.src_path}, rebuilding...")
                os.system(self.build_command)

def start_server():
    app.run(port=PORT, use_reloader=False)

if __name__ == "__main__":
    # Start initial build
    os.system('python main.py')

    # Start the server
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Set up watcher
    event_handler = ChangeHandler('python main.py')
    observer = Observer()
    observer.schedule(event_handler, path=SRC_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
