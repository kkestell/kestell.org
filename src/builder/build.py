import hashlib
import os
import re
import shutil
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

import httpx
import markdown
from jinja2 import Environment, FileSystemLoader, Template
from recipy.markdown import recipe_from_markdown
from recipy.models import Recipe
from recipy.pdf import recipe_to_pdf


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
        with self.filename.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        if lines[0].strip() == "---":
            end_frontmatter_idx = lines[1:].index("---\n") + 1
        else:
            raise ValueError("Frontmatter must start with '---'")

        frontmatter = {}
        for line in lines[1:end_frontmatter_idx]:
            key, value = line.strip().split(": ", 1)
            frontmatter[key] = value

        content = "".join(lines[end_frontmatter_idx + 2 :])

        return Document(frontmatter, content)


class Node:
    def __init__(
        self, name: str, formatted_path: str, original_path: str, order: int = 0
    ):
        self.name = name
        self.formatted_path = formatted_path
        self.original_path = original_path
        self.parent = None
        self.order = order


class Directory(Node):
    def __init__(
        self,
        name: str,
        formatted_path: str,
        original_path: str,
        children: List[Node] = None,
        order: int = 0,
    ):
        super().__init__(name, formatted_path, original_path, order)
        if children is None:
            children = []
        self.children = children

    def add_child(self, child: Node):
        child.parent = self
        self.children.append(child)


class File(Node):
    def __init__(
        self,
        formatted_path: str,
        original_path: str,
        document: Document,
        updated_on: str,
    ):
        super().__init__(
            document.frontmatter.get("title", "Untitled"), formatted_path, original_path
        )
        self.document = document
        self.updated_on = updated_on


class SiteBuilder:
    def __init__(self, input_dir: Path, output_dir: Path, pdf: bool):
        self.content_dir = input_dir / "content"
        self.templates_dir = input_dir / "templates"
        self.static_dir = input_dir / "static"
        self.output_dir = output_dir
        self.root_directory = Directory("Home", "", "")
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.templates_dir)))
        self.cache_file = output_dir / ".build_cache.json"
        self.pdf = pdf
        self.github_username = "kkestell"
        self.github_repos = self._fetch_github_repos()

    def _fetch_github_repos(self):
        url = f"https://api.github.com/users/{self.github_username}/repos"
        params = {"sort": "pushed", "direction": "desc", "per_page": 100}

        repos = []
        page = 1
        six_months_ago = datetime.now() - timedelta(days=180)

        while True:
            response = httpx.get(url, params={**params, "page": page})

            if response.status_code != 200:
                print(
                    f"Error: Unable to fetch repositories. Status code: {response.status_code}"
                )
                return []

            page_repos = response.json()
            if not page_repos:
                break

            for repo in page_repos:
                if repo["fork"] or repo["archived"]:
                    continue
                updated_at = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                if updated_at > six_months_ago:
                    repos.append((repo, updated_at))
                else:
                    return repos

            page += 1

        return repos

    def build(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)
        self._build_structure(self.root_directory, self.content_dir)
        self._build_html(self.root_directory)
        self._build_homepage()
        self._copy_static()

    def _build_structure(self, current_directory: Directory, current_path: Path):
        for item in current_path.iterdir():
            order, name = self._parse_prefix(item.stem)

            formatted_name = name.title()
            original_path = item.relative_to(self.content_dir).as_posix()
            formatted_path = re.sub(r"\d+_", "", original_path)

            if item.is_dir():
                directory = Directory(
                    formatted_name, formatted_path, original_path, order=order
                )
                current_directory.add_child(directory)
                self._build_structure(directory, item)
            elif item.is_file() and item.suffix == ".md":
                document = FrontMatterParser(item).parse()
                if document.frontmatter.get("draft", "false").lower() == "true":
                    continue
                updated_on = datetime.fromtimestamp(item.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                file = File(formatted_path, original_path, document, updated_on)
                current_directory.add_child(file)
        self._sort_structure(current_directory)

    def _parse_prefix(self, name):
        match = re.match(r"^(\d+)_(.*)$", name)
        if match:
            return int(match.group(1)), match.group(2)
        return 0, name

    def _sort_structure(self, directory: Directory):
        directory.children.sort(
            key=lambda n: (
                n.order,
                f"0{n.name}" if isinstance(n, Directory) else f"1{n.name}",
            )
        )
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
                output_file = (self.output_dir / child.formatted_path).with_suffix(
                    ".html"
                )
                self._build_page(child, output_file)

    def _build_index(self, directory: Directory, output_path: Path):
        content = self._generate_list(directory)
        breadcrumbs = self._generate_breadcrumbs(directory)
        template = self.jinja_env.get_template("index.html")
        index_html = template.render(
            content=content, title=directory.name, breadcrumbs=breadcrumbs
        )
        with open(output_path / "index.html", "w", encoding="utf-8") as f:
            f.write(index_html)

    def _build_normal_page(self, template: Template, breadcrumbs: str, file: File):
        content = markdown.markdown(file.document.content, extensions=["extra"])
        html_content = template.render(
            content=content,
            breadcrumbs=breadcrumbs,
            updated_on=file.updated_on,
            **file.document.frontmatter,
        )
        return html_content

    def _generate_pdf(self, recipe: Recipe, pdf_path: Path, source_date_epoch: Optional[str] = "0"):
        pdf_path = self.output_dir / pdf_path
        pdf_data = recipe_to_pdf(recipe, source_date_epoch)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        with pdf_path.open("wb") as f:
            f.write(pdf_data)
        print(pdf_path)

    def _build_recipe_page(self, template: Template, breadcrumbs: str, file: File):
        recipe = recipe_from_markdown(file.document.content)
        if not recipe:
            raise ValueError(f"Failed to parse recipe: {file.original_path}")
        pdf_path = Path(f"static/{file.formatted_path.replace('.md', '.pdf')}")
        if self.pdf:
            # convert date to seconds since epoch e.g. '2024-07-20 22:41:06'
            source_date_epoch = str(int(datetime.strptime(file.updated_on, "%Y-%m-%d %H:%M:%S").timestamp()))
            self._generate_pdf(recipe, pdf_path, source_date_epoch)
        html_content = template.render(
            recipe=recipe,
            pdf_path=pdf_path,
            breadcrumbs=breadcrumbs,
            updated_on=file.updated_on,
            **file.document.frontmatter,
        )
        return html_content

    def _build_page(self, file: File, output_file: Path):
        template_name = file.document.frontmatter.get("template", "page")
        template = self.jinja_env.get_template(f"{template_name}.html")
        breadcrumbs = self._generate_breadcrumbs(file)

        if template_name == "recipe":
            html_content = self._build_recipe_page(template, breadcrumbs, file)
        else:
            html_content = self._build_normal_page(template, breadcrumbs, file)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as f:
            f.write(html_content)

        print(output_file)

    def _build_homepage(self):
        html = []
        for child in self.root_directory.children:
            if isinstance(child, Directory):
                if child.name.lower() == "projects":
                    html.append(f'<div class="list projects">')
                    html.append(f"<h2>Projects</h2>")
                    html.append(self._generate_github_repos_list())
                    html.append("</div>")
                else:
                    dir_name = child.name.lower()
                    html.append(f'<div class="list {dir_name}">')
                    html.append(f"<h2>{child.name}</h2>")
                    html.append(self._generate_list(child))
                    html.append("</div>")
        html = "".join(html)
        home_template = self.jinja_env.get_template("home.html")
        home_html = home_template.render(content=html)
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(home_html)

    def _generate_github_repos_list(self):
        html_builder = ["<ul>"]
        for repo, _ in self.github_repos:
            name = repo["name"]
            description = repo["description"] or "No description"
            language = repo["language"] or "Unknown"
            url = repo["html_url"]
            html_builder.append(
                f'<li><a href="{url}">{name}</a> <small>{language.lower()}</small>'
            )
            html_builder.append(f"<span>{description}</span>")
            html_builder.append("</li>")
        html_builder.append("</ul>")
        return "".join(html_builder)

    def _copy_static(self):
        target_dir = self.output_dir / "static"
        target_dir.mkdir(parents=True, exist_ok=True)

        for item in os.listdir(self.static_dir):
            s = Path(self.static_dir) / item
            d = target_dir / item
            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

    def _generate_list(self, directory: Directory):
        html_builder = ["<ul>"]
        for child in directory.children:
            if isinstance(child, Directory):
                dir_link = f"/{child.formatted_path}/index.html"
                html_builder.append(
                    f'<li class="dir"><h2><a href="{dir_link}">{child.name}</a></h2>{self._generate_list(child)}</li>'
                )
            elif isinstance(child, File):
                page_path = child.formatted_path.replace(".md", ".html")
                title = child.name
                html_builder.append(f'<li><a href="/{page_path}">{title}</a>')
                if child.document.frontmatter.get("subtitle"):
                    html_builder.append(
                        f"<span>{child.document.frontmatter['subtitle']}</span>"
                    )
                html_builder.append("</li>")
        html_builder.append("</ul>")
        return "".join(html_builder)

    def _generate_breadcrumbs(self, node: Node):
        breadcrumbs = []
        current_node = node.parent
        while current_node:
            breadcrumbs.append(
                f'<a href="/{current_node.formatted_path}">{current_node.name}</a>'
            )
            current_node = current_node.parent
        breadcrumbs = breadcrumbs[::-1]
        breadcrumbs.append(node.name)
        return ' <span class="separator">/</span> '.join(breadcrumbs)


def main():
    parser = ArgumentParser(description="Static site generator")
    parser.add_argument("-i", "--input", default="./site/", help="Input directory path")
    parser.add_argument(
        "-o", "--output", default="./dist/", help="Output directory path"
    )
    parser.add_argument(
        "-p", "--pdf", action="store_true", help="Generate PDFs for recipe pages"
    )
    args = parser.parse_args()

    builder = SiteBuilder(Path(args.input), Path(args.output), args.pdf)
    builder.build()


if __name__ == "__main__":
    main()
