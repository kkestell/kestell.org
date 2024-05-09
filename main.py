from datetime import datetime
from argparse import ArgumentParser
from pathlib import Path
import shutil
from string import Template
from typing import List
import markdown
import requests
from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
import re


class EmbedPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            match = re.search(r"\[\[(https?://[^\s\]]+)]]", line)
            if match:
                url = match.group(1)
                url_content = requests.get(url).text
                url_content_lines = url_content.split('\n')
                new_lines.append("<!-- EMBED {} -->".format(url))
                new_lines.extend(url_content_lines)
                new_lines.append("<!-- /EMBED -->")
            else:
                new_lines.append(line)
        return new_lines


class EmbedPostprocessor(Postprocessor):
    def run(self, text):
        new_text = []
        embed = False
        for line in text.split('\n'):
            if line.startswith("<!-- EMBED"):
                embed = True
                url = line.split(' ')[2]
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_text.append(
                    f'<div class="embed"><p>Embedded from <a href="{url}">{url}</a> on {now}</p><div class="embed-content">')
            elif line.startswith("<!-- /EMBED"):
                embed = False
                new_text.append('</div></div>')
            elif embed:
                new_text.append(line)
            else:
                new_text.append(line)
        return '\n'.join(new_text)


class EmbedPreprocessorExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(EmbedPreprocessor(md), 'norender', 1000)


class EmbedPostprocessorExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(EmbedPostprocessor(md), 'norender', 10)


class Document:
    def __init__(self, frontmatter, content):
        self.frontmatter = frontmatter
        self.content = content


class FrontMatterParser:
    def __init__(self, filename):
        self.filename = Path(filename)

    def parse(self):
        with self.filename.open('r', encoding='utf-8') as file:
            lines = file.readlines()

        if lines[0].strip() == '---':
            end_frontmatter_idx = lines[1:].index('---\n') + 1
        else:
            raise ValueError("Frontmatter must start with '---'")

        frontmatter = {}
        for line in lines[1:end_frontmatter_idx]:
            key, value = line.strip().split(': ', 1)
            frontmatter[key] = value

        content = ''.join(lines[end_frontmatter_idx + 2:])

        return Document(frontmatter, content)


class Node:
    def __init__(self, name: str, path: str, order: int = 0):
        self.name = name
        self.path = path
        self.parent = None
        self.order = order


class Directory(Node):
    def __init__(self, name: str, path: str, children: List[Node] = None, order: int = 0):
        super().__init__(name, path, order)
        if children is None:
            children = []
        self.children = children

    def add_child(self, child: Node):
        child.parent = self
        self.children.append(child)


class File(Node):
    def __init__(self, path: str, document: Document, updated_on: str):
        super().__init__(document.frontmatter.get('title', 'Untitled'), path)
        self.document = document
        self.updated_on = updated_on


class SiteBuilder:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.content_dir = input_dir / 'content'
        self.templates_dir = input_dir / 'templates'
        self.static_dir = input_dir / 'static'
        self.output_dir = output_dir
        self.root_directory = Directory('Home', '')
        self.templates = self._cache_templates()
        self._cache_templates()

    def build(self):
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._build_structure(self.root_directory, self.content_dir)
        self._build_html(self.root_directory)
        self._build_homepage()
        self._copy_static()

    def _build_structure(self, current_directory: Directory, current_path: Path):
        for item in current_path.iterdir():
            order, name = self._parse_prefix(item.stem)

            formatted_name = name.title()
            formatted_path = item.relative_to(self.content_dir).as_posix()
            formatted_path = re.sub(r'\d+_', '', formatted_path)

            if item.is_dir():
                directory = Directory(formatted_name, formatted_path, order=order)
                current_directory.add_child(directory)
                self._build_structure(directory, item)
            elif item.is_file() and item.suffix == '.md':
                document = FrontMatterParser(item).parse()
                if document.frontmatter.get('draft', 'false').lower() == 'true':
                    continue
                updated_on = datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                file = File(formatted_path, document, updated_on)
                current_directory.add_child(file)
        self._sort_structure(current_directory)

    def _parse_prefix(self, name):
        match = re.match(r'^(\d+)_(.*)$', name)
        if match:
            return int(match.group(1)), match.group(2)
        return 0, name

    def _sort_structure(self, directory: Directory):
        directory.children.sort(key=lambda n: (n.order, f"0{n.name}" if isinstance(n, Directory) else f"1{n.name}"))
        for child in directory.children:
            if isinstance(child, Directory):
                self._sort_structure(child)

    def _build_html(self, current_directory: Directory):
        for child in current_directory.children:
            if isinstance(child, Directory):
                directory_path = self.output_dir / child.path
                directory_path.mkdir(parents=True, exist_ok=True)
                self._build_html(child)
                self._build_index(child, directory_path)
            elif isinstance(child, File):
                output_file = (self.output_dir / child.path).with_suffix('.html')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                self._build_page(child, output_file)

    def _build_index(self, directory: Directory, output_path: Path):
        content = self._generate_list(directory)
        breadcrumbs = self._generate_breadcrumbs(directory)
        template = self._load_template('index')
        index_html = template.substitute(content=content, title=directory.name, breadcrumbs=breadcrumbs)
        with open(output_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)

    def _build_page(self, file: File, output_file: Path):
        content = markdown.markdown(file.document.content,
                                    extensions=['extra', EmbedPreprocessorExtension(), EmbedPostprocessorExtension()])
        template_name = file.document.frontmatter.get('template', 'page')
        template = self._load_template(template_name)
        breadcrumbs = self._generate_breadcrumbs(file)
        html_content = template.substitute(content=content, breadcrumbs=breadcrumbs, updated_on=file.updated_on,
                                           **file.document.frontmatter)
        with output_file.open('w', encoding='utf-8') as f:
            f.write(html_content)

    def _build_homepage(self):
        content = self._generate_list(self.root_directory)
        home_template = self._load_template('home')
        home_html = home_template.substitute(content=content)
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(home_html)

    def _copy_static(self):
        shutil.copytree(self.static_dir, self.output_dir / 'static')

    def _generate_list(self, directory: Directory):
        html_builder = ["<div class=\"list\"><ul>"]
        for child in directory.children:
            if isinstance(child, Directory):
                dir_link = f"/{child.path}/index.html"
                html_builder.append(
                    f"<li class=\"dir\"><a href=\"{dir_link}\">{child.name}</a>{self._generate_list(child)}</li>")
            elif isinstance(child, File):
                page_path = child.path.replace('.md', '.html')
                title = child.name
                html_builder.append(f"<li><a href=\"/{page_path}\">{title}</a>")
                if child.document.frontmatter.get('subtitle'):
                    html_builder.append(f"<br><span>{child.document.frontmatter['subtitle']}</span>")
                html_builder.append("</li>")
        html_builder.append("</ul></div>")
        return ''.join(html_builder)

    def _generate_breadcrumbs(self, node: Node):
        breadcrumbs = []
        current_node = node.parent
        while current_node:
            breadcrumbs.append(f"<a href=\"/{current_node.path}\">{current_node.name}</a>")
            current_node = current_node.parent
        breadcrumbs = breadcrumbs[::-1]
        breadcrumbs.append(node.name)
        return ' <span class="separator">/</span> '.join(breadcrumbs)

    def _cache_templates(self):
        templates = {}
        template_dir = self.templates_dir
        for template_file in template_dir.glob('*.html'):
            with template_file.open('r', encoding='utf-8') as file:
                templates[template_file.stem] = Template(file.read())
        return templates

    def _load_template(self, name):
        return self.templates[name]


def main():
    parser = ArgumentParser(description="Static site generator")
    parser.add_argument('-i', '--input', default='./src/', help='Input directory path')
    parser.add_argument('-o', '--output', default='./dist/', help='Output directory path')
    args = parser.parse_args()

    builder = SiteBuilder(Path(args.input), Path(args.output))
    builder.build()


if __name__ == "__main__":
    main()
