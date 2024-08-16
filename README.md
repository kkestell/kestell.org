# kestell.org

# `build.py`

## Overview

Generates a static website from markdown files, building the site structure and converting content to HTML and optionally PDFs for recipe pages.

## Usage

```bash
python build.py [options]
```

### Options

<dl>
  <dt><code>-i, --input</code></dt>
  <dd>Input directory path (default: <code>./site/</code>)</dd>

  <dt><code>-o, --output</code></dt>
  <dd>Output directory path (default: <code>./dist/</code>)</dd>

  <dt><code>-p, --pdf</code></dt>
  <dd>Generate PDFs for recipe pages</dd>
</dl>

### Examples

### Build the Site with Default Settings

```bash
python build.py
```

Generates the site using the default input (`./site/`) and output (`./dist/`) directories.

### Build the Site and Generate PDFs for Recipes

```bash
python build.py -p
```

Generates the site and also creates PDFs for recipe pages.

### Build the Site with Custom Input and Output Directories

```bash
python build.py -i "./custom_site/" -o "./custom_dist/"
```

Uses `./custom_site/` as the input directory and outputs the generated site to `./custom_dist/`.

# `watch.py`

## Overview

Monitors the `site` directory for changes and automatically rebuilds the project using `build.py`. The script also serves the `dist` directory via a Flask web server.

## Usage

```bash
pdm run src/builder/watch.py [options]
```

### Options

<dl>
  <dt><code>-i, --input</code></dt>
  <dd>Input directory path (default: <code>./site/</code>)</dd>

  <dt><code>-o, --output</code></dt>
  <dd>Output directory path (default: <code>./dist/</code>)</dd>

  <dt><code>-p, --port</code></dt>
  <dd>Port to run the server on (default: <code>8080</code>)</dd>

  <dt><code>-b, --build-command</code></dt>
  <dd>Command to run on file changes (default: <code>pdm run src/builder/build.py</code>)</dd>
</dl>

## Examples

### Start the Script with Default Settings

```bash
pdm run src/builder/watch.py
```

Starts the server on port 8080, monitors the `./site/` directory for changes, and serves files from `./dist/`.

### Start the Script with Custom Input and Output Directories

```bash
pdm run src/builder/watch.py -i "./custom_site/" -o "./custom_dist/"
```

Monitors the `./custom_site/` directory and serves files from `./custom_dist/`.

### Start the Script on a Different Port

```bash
pdm run src/builder/watch.py -p 9090
```

Starts the server on port 9090 instead of the default 8080.

## Notes

* File changes are debounced to prevent multiple rebuilds from rapid successive changes.
* The Flask server automatically serves the `index.html` file for the root URL.

# `scaffold.py`

## Overview

Scaffold pages. Currently, only recipes are supported.

## Usage

```bash
pdm run src/builder/scaffold.py recipe [options]
```

### Options

<dl>
  <dt><code>-i, --input</code></dt>
  <dd>Input directory (default: <code>./site/</code>)</dd>

  <dt><code>-c, --category</code></dt>
  <dd>Category name (default: <code>misc</code>).</dd>

  <dt><code>-t, --title</code></dt>
  <dd>Title of the document (default: <code>Untitled</code>).</dd>

  <dt><code>-u, --url</code></dt>
  <dd>URL to fetch the recipe from.</dd>
</dl>

## Examples

### Create a Recipe with Default Settings

```bash
pdm run src/builder/scaffold.py recipe
```

Creates a file in e.g. `./site/content/2_recipes/10_misc/untitled.md` with the default content structure.

### Create a Recipe with a Specific Category and Title

```bash
pdm run src/builder/scaffold.py recipe -c "breakfast" -t "Pancakes"
```

Resolves to the directory e.g. `1_breakfast` and creates the file with the specified title.

### Create a Recipe with Content from a URL

```bash
pdm run src/builder/scaffold.py recipe -u "https://example.com/recipe"
```

Fetches the content from the URL and places it below the frontmatter.

## Notes

* The script automatically handles category directories with leading digits.
* The `content` subdirectory is hardcoded in the file path structure.
