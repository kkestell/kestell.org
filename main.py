import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import List

import markdown
from jinja2 import Environment, FileSystemLoader, Template

from recipes import parse_recipe_markdown, RecipeModel, recipe_to_latex


class Document:
    def __init__(self, frontmatter, content):
        self.frontmatter = frontmatter
        self.content = content
        self.content_hash = self._hash_content()

    def _hash_content(self):
        return hashlib.md5(self.content.encode()).hexdigest()


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
    def __init__(self, name: str, formatted_path: str, original_path: str, order: int = 0):
        self.name = name
        self.formatted_path = formatted_path
        self.original_path = original_path
        self.parent = None
        self.order = order


class Directory(Node):
    def __init__(self, name: str, formatted_path: str, original_path: str, children: List[Node] = None, order: int = 0):
        super().__init__(name, formatted_path, original_path, order)
        if children is None:
            children = []
        self.children = children

    def add_child(self, child: Node):
        child.parent = self
        self.children.append(child)


class File(Node):
    def __init__(self, formatted_path: str, original_path: str, document: Document, updated_on: str):
        super().__init__(document.frontmatter.get('title', 'Untitled'), formatted_path, original_path)
        self.document = document
        self.updated_on = updated_on


class SiteBuilder:
    def __init__(self, input_dir: Path, output_dir: Path, force: bool, pdf: bool):
        self.content_dir = input_dir / 'content'
        self.templates_dir = input_dir / 'templates'
        self.static_dir = input_dir / 'static'
        self.output_dir = output_dir
        self.root_directory = Directory('Home', '', '')
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.templates_dir)))
        self.cache_file = output_dir / '.build_cache.json'
        self.file_cache = {} if force else self._load_cache()
        self.pdf = pdf

    def _load_cache(self):
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.file_cache, f)

    def build(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self._build_structure(self.root_directory, self.content_dir)
        self._build_html(self.root_directory)
        self._build_homepage()
        self._copy_static()
        self._save_cache()

    def _build_structure(self, current_directory: Directory, current_path: Path):
        for item in current_path.iterdir():
            order, name = self._parse_prefix(item.stem)

            formatted_name = name.title()
            original_path = item.relative_to(self.content_dir).as_posix()
            formatted_path = re.sub(r'\d+_', '', original_path)

            if item.is_dir():
                directory = Directory(formatted_name, formatted_path, original_path, order=order)
                current_directory.add_child(directory)
                self._build_structure(directory, item)
            elif item.is_file() and item.suffix == '.md':
                document = FrontMatterParser(item).parse()
                if document.frontmatter.get('draft', 'false').lower() == 'true':
                    continue
                updated_on = datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                file = File(formatted_path, original_path, document, updated_on)
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
                directory_path = self.output_dir / child.formatted_path
                directory_path.mkdir(parents=True, exist_ok=True)
                self._build_html(child)
                self._build_index(child, directory_path)
            elif isinstance(child, File):
                output_file = (self.output_dir / child.formatted_path).with_suffix('.html')
                self._build_page(child, output_file)

    def _build_index(self, directory: Directory, output_path: Path):
        content = self._generate_list(directory)
        breadcrumbs = self._generate_breadcrumbs(directory)
        template = self.jinja_env.get_template('index.html')
        index_html = template.render(content=content, title=directory.name, breadcrumbs=breadcrumbs)
        with open(output_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)

    def _build_normal_page(self, template: Template, breadcrumbs: str, file: File):
        content = markdown.markdown(file.document.content, extensions=['extra'])
        html_content = template.render(content=content, breadcrumbs=breadcrumbs, updated_on=file.updated_on, **file.document.frontmatter)
        return html_content

    def _generate_pdf(self, recipe: RecipeModel, pdf_path: str):
        pdf_path = self.output_dir / pdf_path.lstrip('/')
        latex_content = recipe_to_latex(recipe)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, 'recipe.tex')
            with open(temp_file, 'w') as f:
                f.write(latex_content)
            subprocess_args = ['xelatex', temp_file, '-output-directory', temp_dir]
            subprocess.run(subprocess_args, cwd=temp_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            temp_path = os.path.join(temp_dir, 'recipe.pdf')
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(temp_path, pdf_path)

    def _build_recipe_page(self, template: Template, breadcrumbs: str, file: File):
        recipe = parse_recipe_markdown(file.document.content)
        if not recipe:
            raise ValueError(f"Failed to parse recipe: {file.original_path}")
        pdf_path = f"/static/{file.formatted_path.replace('.md', '.pdf')}"
        if self.pdf:
            self._generate_pdf(recipe, pdf_path)
        html_content = template.render(recipe=recipe, pdf_path=pdf_path, breadcrumbs=breadcrumbs, updated_on=file.updated_on, **file.document.frontmatter)
        return html_content

    def _build_page(self, file: File, output_file: Path):
        cached_info = self.file_cache.get(file.original_path, {})
        cached_hash = cached_info.get('content_hash')
        current_hash = file.document.content_hash

        if output_file.exists() and cached_hash == current_hash:
            return

        template_name = file.document.frontmatter.get('template', 'page')
        template = self.jinja_env.get_template(f'{template_name}.html')
        breadcrumbs = self._generate_breadcrumbs(file)

        if template_name == 'recipe':
            html_content = self._build_recipe_page(template, breadcrumbs, file)
        else:
            html_content = self._build_normal_page(template, breadcrumbs, file)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open('w', encoding='utf-8') as f:
            f.write(html_content)

        # Update the cache
        self.file_cache[file.original_path] = {
            'content_hash': current_hash,
            'mtime': os.path.getmtime(self.content_dir / file.original_path),
            'formatted_path': file.formatted_path
        }

    def _build_homepage(self):
        content = self._generate_list(self.root_directory)
        home_template = self.jinja_env.get_template('home.html')
        home_html = home_template.render(content=content)
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(home_html)

    def _copy_static(self):
        target_dir = self.output_dir / 'static'
        target_dir.mkdir(parents=True, exist_ok=True)

        for item in os.listdir(self.static_dir):
            s = Path(self.static_dir) / item
            d = target_dir / item
            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    def _generate_list(self, directory: Directory):
        html_builder = ["<div class=\"list\"><ul>"]
        for child in directory.children:
            if isinstance(child, Directory):
                dir_link = f"/{child.formatted_path}/index.html"
                html_builder.append(
                    f"<li class=\"dir\"><a href=\"{dir_link}\">{child.name}</a>{self._generate_list(child)}</li>")
            elif isinstance(child, File):
                page_path = child.formatted_path.replace('.md', '.html')
                title = child.name
                html_builder.append(f"<li><a href=\"/{page_path}\">{title}</a>")
                if child.document.frontmatter.get('subtitle'):
                    html_builder.append(f"<span>{child.document.frontmatter['subtitle']}</span>")
                html_builder.append("</li>")
        html_builder.append("</ul></div>")
        return ''.join(html_builder)

    def _generate_breadcrumbs(self, node: Node):
        breadcrumbs = []
        current_node = node.parent
        while current_node:
            breadcrumbs.append(f"<a href=\"/{current_node.formatted_path}\">{current_node.name}</a>")
            current_node = current_node.parent
        breadcrumbs = breadcrumbs[::-1]
        breadcrumbs.append(node.name)
        return ' <span class="separator">/</span> '.join(breadcrumbs)


def main():
    parser = ArgumentParser(description="Static site generator")
    parser.add_argument('-i', '--input', default='./src/', help='Input directory path')
    parser.add_argument('-o', '--output', default='./dist/', help='Output directory path')
    parser.add_argument('-f', '--force', action='store_true', help='Force rebuild of all files')
    parser.add_argument('-p', '--pdf', action='store_true', help='Generate PDFs for recipe pages')
    args = parser.parse_args()

    builder = SiteBuilder(Path(args.input), Path(args.output), args.force, args.pdf)
    builder.build()


if __name__ == "__main__":
    main()
