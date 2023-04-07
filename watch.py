import argparse
import http.server
import subprocess
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from time import time
from typing import List

from bs4 import BeautifulSoup as bs
from jinja2 import Environment, FileSystemLoader
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

last_trigger_time = time()


@contextmanager
def http_server(host: str, port: int, directory: str):
    server = http.server.ThreadingHTTPServer(
        (host, port), partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    )
    server_thread = threading.Thread(target=server.serve_forever, name="http_server")
    server_thread.start()

    try:
        yield
    finally:
        server.shutdown()
        server_thread.join()


class FileSystemHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type not in ["created", "modified", "deleted"]:
            return
        global last_trigger_time
        current_time = time()
        if event.src_path.find("~") == -1 and (current_time - last_trigger_time) > 1:
            last_trigger_time = current_time
            subprocess.run(["python3", "build.py"])
           


class Watcher:
    def __init__(self, args):
        self.observer = Observer()
        self.handler = FileSystemHandler()
        self.observer.schedule(self.handler, "content", recursive=True)
        self.observer.schedule(self.handler, "templates", recursive=True)
        self.observer.schedule(self.handler, "static", recursive=True)

    def watch(self):
        with http_server("localhost", 1313, "build"):
            self.observer.start()
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                self.observer.stop()
                self.observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TODO")

    args = parser.parse_args()

    watcher = Watcher(args)
    watcher.watch()