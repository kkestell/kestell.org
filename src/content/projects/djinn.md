---
title: "Djinn"
subtitle: "Soulseek + MusicBrainz."
date: 2023-05-29
draft: false
---

Djinn downloads music from [Soulseek](https://www.slsknet.org/) and tags it with data from [MusicBrainz](https://musicbrainz.org/). Djinn can download a single release, or an artist's entire discography.

## Features

* Uses `TagLib`, `eyeD3`, and `metaflac` to tag MP3 and FLAC files.
* Automatically downloads cover art from MusicBrainz and Last.fm.
* Configurable directory and file names.

## Examples

Download a single release:

```bash
djinn download --release 1b022e8e-4da6-4f9a-8f3d-3d3f2f0f3b6f
```

Download an artist's discography:

```bash
djinn download --artist 1b022e8e-4da6-4f9a-8f3d-3d3f2f0f3b6f
```

Download a single release, limiting downloads to .mp3 files, and replacing existing files:

```bash
djinn download --release 1b022e8e-4da6-4f9a-8f3d-3d3f2f0f3b6f --file-types .mp3 --replace
```

## Source

The source code for Djinn is available on [GitHub](https://github.com/kkestell/djinn).

## License

Djinn uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
