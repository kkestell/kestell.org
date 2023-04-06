import frontmatter
from jinja2 import Environment, FileSystemLoader
import markdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup as bs

import argparse
from pathlib import Path
from time import time
import http.server
import socketserver
import signal
import shutil


def build_page(file, template, output_dir):
    post = frontmatter.load(file)
    content = markdown.markdown(post.content, extensions=['fenced_code', 'codehilite', 'footnotes', 'tables', 'smarty', 'def_list'])
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template)
    html = template.render(content=content, **post.metadata)
    output_file = output_dir / file.with_suffix('.html').name
    with open(output_file, 'w') as f:
        f.write(html)
    return {
        'title': post.metadata['title'],
        'description': post.metadata['description'],
        'created': post.metadata['created'],
        'updated': post.metadata['updated'],
        'path': output_file.relative_to(output_dir)
    }


def build_index(pages, output_dir):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html.j2')

    pages.sort(key=lambda page: page['updated'], reverse=True)

    output = template.render(pages=pages)

    output = prettify_html(output)

    output_file = output_dir / 'index.html'
    output_file.write_text(output)


def prettify_html(html):
    soup = bs(html, 'html.parser')
    return soup.prettify()


def build(args):
    try:
        if args.out.exists():
            shutil.rmtree(args.out)
        args.out.mkdir(parents=True, exist_ok=True)
        start_time = time()
        pages = []
        for file in args.content.glob('*.md'):
            page = build_page(file, 'show.html.j2', args.out)
            pages.append(page)
        build_index(pages, args.out)
        end_time = time()
        copy_static_files(args)
        print(f'Build took {int((end_time - start_time) * 1000)}ms')
    except Exception as e:
        print(e)


def copy_static_files(args):
    shutil.copytree('static', args.out / 'static')


last_trigger_time = time()
PORT = 1313


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *xargs, **kwargs):
        super().__init__(*xargs, directory=args.out, **kwargs)


class FileSystemHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type not in ['created', 'modified', 'deleted']:
            return
        global last_trigger_time
        current_time = time()
        if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
            last_trigger_time = current_time
            build(args)


def watch(args):
    with socketserver.TCPServer(("", args.port), HttpHandler) as httpd:
        handler = FileSystemHandler()
        observer = Observer()
        observer.schedule(handler, args.content, recursive=True)
        observer.schedule(handler, 'templates', recursive=True)
        observer.schedule(handler, 'static', recursive=True)
        observer.start()

        def shutdown(*args):
            httpd._BaseServer__shutdown_request = True
            observer.stop()

        signal.signal(signal.SIGINT, shutdown)

        print(f"Listening on port {args.port}...")

        httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')

    parser.add_argument('command', choices=['build', 'watch'], help='Command to run')
    parser.add_argument('--content', type=Path, default='content', help='Path to content directory')
    parser.add_argument('--out', type=Path, default='build', help='Path to output directory')
    parser.add_argument('--port', type=int, default=1313, help='Port to serve on')

    args = parser.parse_args()

    if args.command == 'build':
        build(args)
    elif args.command == 'watch':
        build(args)
        watch(args)
