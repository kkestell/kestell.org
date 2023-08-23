---
title: "Colophon"
subtitle: "About the software that runs this site"
date: 2023-04-27
draft: false
---

This site is built using a custom static site generator written in C#. Markdown conversion is handled by [Markdig](), [YamlDotNet]() is used for YAML parsing, and templating is done using [Handlebars.Net](). PDFs are generated using [Pandoc]().

Pages are written in Markdown with YAML front matter. The front matter is used to specify the page title, subtitle, date, and whether or not the page is a draft.

## CLI

The CLI supports two commands: `build` and `serve`.

The `build` command builds the site.

```shell
$ builder build --root ./src --output ./dist
```

The `serve` command starts a local web server and automatically rebuilds the site when files change.

```shell
$ builder serve --root ./src --output ./dist --port 8080
```

Both the `build` and `serve` commands accept optional `--drafts` and `--pdfs` arguments which include draft posts in the build and control PDF generation, respectively.

## Misc. Notes

An `install.sh` script is included in the root of the repository. This script AOT compiles the builder CLI and copies it to `~/.local/bin`.

## Source

The source code for Builder is available on [GitHub](https://github.com/kkestell/kestell.org).

## License

Builder uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.