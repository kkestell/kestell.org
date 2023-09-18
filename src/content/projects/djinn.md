---
title: "Djinn"
subtitle: "Soulseek + MusicBrainz."
date: 2023-05-29
draft: false
---

Djinn downloads music using [Soulseek](https://www.slsknet.org/) using metadata from [MusicBrainz](https://musicbrainz.org/) and [Last.fm](https://www.last.fm/). Djinn can download a single release, or an artist's entire discography.

## Features

* Uses `TagLib`, `eyeD3`, and `metaflac` to tag MP3 and FLAC files.
* Automatically downloads cover art from MusicBrainz and Last.fm.
* Configurable directory and file names.

## Usage

```
$ djinn download --help

Description:
  Download one or more releases

Usage:
  djinn download [options]

Options:
  --release-id <release-id>        Release ID
  --release-title <release-title>  Release title
  --artist-id <artist-id>          Artist ID
  --artist-name <artist-name>      Artist name
  --replace                        Replace existing album(s)
  --file-types <file-types>        File types to download [default: .flac|.mp3]
  --verbose                        Verbose output
  --no-progress                    Disable realtime download progress
  --year <year>                    Release year
  --strip-existing-metadata        Strip existing metadata from downloaded files [default: True]
  -?, -h, --help                   Show help and usage information
```

```
$ djinn upgrade --help
Description:
  Replace mp3 files with flac files

Usage:
  djinn upgrade [options]

Options:
  --randomize     Randomize download order
  --verbose       Verbose output
  -?, -h, --help  Show help and usage information
```

## Examples

Download a single release by ID:

```shell
$ djinn download --release-id "1b022e8e-4da6-4f9a-8f3d-3d3f2f0f3b6f"
```

Download a single release by title:

<pre><code>$ djinn download --release-title "Abbey Road"

Please select the correct release group for Abbey Road:
<span style="color: #aaa">  Abbey's Road                    Ada Montellanico, Giovanni Falzone              2016
  Abbey Road                      Various Artists                                 2012</span>
<span style="color: yellow">&gt; Abbey Road                      The Beatles                                     1969</span>
<span style="color: #aaa">  Abbey Road Live                 Colin Vearncombe                                2000
  Neath Abbey Road                The Tunnelrunners                               2018
  Off Abbey Road                  Mike Westbrook Band                             1989
  Plays Abbey Road                Devil's Rubato Band, Gustav Peter Wöhler        1995</span></code></pre>

Download an artist's discography by ID:

```shell
$ djinn download --artist-id "1b022e8e-4da6-4f9a-8f3d-3d3f2f0f3b6f"
```

Download an artist's discography by name:

<pre><code>$ djinn download --artist-name "The Beatles"

Please select the correct artist for The Beatles:
<span style="color: yellow">&gt; The Beatles                     UK rock band, “The Fab Four”</span>
<span style="color: #aaa">  The Beatles                     punk/lofi; published on Whe...
  The Beatles                     1960s Philadelphia doo-wop ...
  The Beatles                     SiIvaGunner collaboration     
  The Beatles Connection          Beatles Tribute Band          
  Not The Beatles                 
  The Beatles Revival             Czech 'The Beatles' tribute...</span></code></pre>

Download a single release, limiting downloads to .mp3 files, and replacing existing files:

```shell
$ djinn download --release-title "Cryptic Writings" --file-types .mp3 --replace
```

Scan your music library for albums in mp3 format and attempt to download replacements in flac format:

```shell
$ djinn upgrade
```

## Source

The source code for Djinn is available on [GitHub](https://github.com/kkestell/djinn).

## License

Djinn uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
