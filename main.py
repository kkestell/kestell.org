import argparse
import http.server
import shutil
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from time import time
from typing import List

import frontmatter
import markdown
from bs4 import BeautifulSoup as bs
from jinja2 import Environment, FileSystemLoader
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


@dataclass
class Page:
    title: str
    description: str
    created: str
    updated: str
    path: Path


@dataclass
class Category:
    name: str
    path: Path
    pages: List[Page]


class SiteBuilder:
    def __init__(self, args):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.args = args

    def load_page(self, file):
        page = frontmatter.load(file)
        return page

    def convert_markdown_to_html(self, page_content):
        content = markdown.markdown(
            page_content,
            extensions=[
                "fenced_code",
                "codehilite",
                "footnotes",
                "tables",
                "smarty",
                "def_list",
                "toc",
            ],
        )
        return content

    def render_template(self, template, template_args):
        template = self.env.get_template(template)
        html = template.render(template_args)
        if self.args.pretty:
            html = self.prettify_html(html)
        return html

    def build_page(self, file, category):
        page = self.load_page(file)
        content = self.convert_markdown_to_html(page.content)
        html = self.render_template("show.html.j2", { "content": content, "metadata": page.metadata, "category": category })
        output_dir = self.args.out / file.parent.relative_to(self.args.content)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{file.stem}.html"
        with open(output_file, "w") as f:
            f.write(html)
        print(output_file.name)
        return Page(
            title=page.metadata["title"],
            description=page.metadata["description"],
            created=page.metadata["created"],
            updated=page.metadata["updated"],
            path='/' / output_file.relative_to(self.args.out)
        )

    def build_category_index(self, category):
        output = self.render_template("index.html.j2", { "category_name": category.name, "pages": category.pages })
        output_file = self.args.out / category.name / "index.html"
        output_file.write_text(output)
        print(output_file.name)

    def build_home(self, categories):
        for category in categories:
            category.pages = category.pages[:3]
        output = self.render_template("home.html.j2", { "categories": categories })
        output_file = self.args.out / "index.html"
        output_file.write_text(output)
        print(output_file.name)

    @staticmethod
    def prettify_html(html):
        soup = bs(html, "html.parser")
        return soup.prettify()

    def process_categories(self):
        categories = []
        for category_directory in self.args.content.glob("*"):
            if not category_directory.is_dir():
                continue
            category = Category(path='/' / category_directory.relative_to(args.content), name=category_directory.name, pages=[])
            for file in category_directory.glob("*.md"):
                page = self.build_page(file, category)
                category.pages.append(page)
            category.pages.sort(key=lambda page: page.updated, reverse=True)
            self.build_category_index(category)
            categories.append(category)
        return categories

    def build(self):
        start_time = time()
        categories = self.process_categories()
        self.build_home(categories)
        end_time = time()
        print(f"Build took {int((end_time - start_time) * 1000)}ms")


def copy_static_files(args):
    start_time = time()
    shutil.copytree("static", args.out / "static", dirs_exist_ok=True)
    end_time = time()
    print(f"Copy static files took {int((end_time - start_time) * 1000)}ms")

last_trigger_time = time()


class FileSystemHandler(FileSystemEventHandler):
    def __init__(self, builder):
        self.builder = builder

    def on_any_event(self, event):
        if event.event_type not in ["created", "modified", "deleted"]:
            return
        global last_trigger_time
        current_time = time()
        if event.src_path.find("~") == -1 and (current_time - last_trigger_time) > 1:
            last_trigger_time = current_time
            self.builder.build()

            # if event.src_path.endswith(".md") or event.src_path.startswith("templates"):
            #     print(f"File {event.src_path} {event.event_type}")
            #     build(args)
            # elif event.src_path.startswith("static"):
            #     print(f"File {event.src_path} {event.event_type}")
            #     copy_static_files(args)


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


class Watcher:
    def __init__(self, args):
        self.builder = SiteBuilder(args)
        self.observer = Observer()
        self.handler = FileSystemHandler(self.builder)
        self.observer.schedule(self.handler, args.content, recursive=True)
        self.observer.schedule(self.handler, "templates", recursive=True)
        self.observer.schedule(self.handler, "static", recursive=True)

    def watch(self):
        with http_server("localhost", self.builder.args.port, self.builder.args.out):
            self.builder.build()
            self.observer.start()
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                self.observer.stop()
                self.observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TODO")

    parser.add_argument("command", choices=["build", "watch"], help="Command to run")
    parser.add_argument(
        "--content", type=Path, default="content", help="Path to content directory"
    )
    parser.add_argument(
        "--out", type=Path, default="build", help="Path to output directory"
    )
    parser.add_argument("--pretty", action="store_true", help="Prettify HTML")
    parser.add_argument("--port", type=int, default=1313, help="Port to serve on")

    args = parser.parse_args()

    if args.command == "build":
        builder = SiteBuilder(args)
        builder.build()
    elif args.command == "watch":
        watcher = Watcher(args)
        watcher.watch()