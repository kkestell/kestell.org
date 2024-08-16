import argparse
from slugify import slugify
from pathlib import Path
from datetime import datetime
import subprocess


def find_category_path(base_dir: Path, category: str) -> str:
    for subdir in base_dir.iterdir():
        if subdir.is_dir() and subdir.name.endswith(f"_{category}"):
            return subdir.name
    raise ValueError(f"Category '{category}' not found in {base_dir}")


def create_recipe(input_dir: str, category: str, title: str, url: str = None):
    base_dir = Path(input_dir) / "content" / "2_recipes"
    category_dir = find_category_path(base_dir, category)

    slugified_title = slugify(title)
    file_path = base_dir / category_dir / f"{slugified_title}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    frontmatter = f"""---
title: {title}
date: {datetime.now().strftime('%Y-%m-%d')}
draft: false
template: recipe
---
"""

    if url:
        result = subprocess.run(['rf', '-f', 'md', url], capture_output=True, text=True)
        content = frontmatter + "\n" + result.stdout
    else:
        content = f"""{frontmatter}
# {title}

## Ingredients

* 

## Instructions

1. 
"""

    file_path.write_text(content)
    print(f"File created: {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Static site generator scaffold.")
    subparsers = parser.add_subparsers(dest='command', help="Subcommands")

    recipe_parser = subparsers.add_parser('recipe', help="Create a new recipe markdown file.")
    recipe_parser.add_argument('-i', '--input', default='./site/', help='Input directory')
    recipe_parser.add_argument('-c', '--category', default='misc', help='Category name')
    recipe_parser.add_argument('-t', '--title', default='Untitled', help='Title of the document')
    recipe_parser.add_argument('-u', '--url', help='URL to fetch content from')

    recipe_parser.set_defaults(func=create_recipe)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args.input, args.category, args.title, args.url)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
