---
title: "Djinn"
subtitle: "Soulseek + MusicBrainz."
date: 2023-05-29
draft: false
---

Djinn downloads albums from [Soulseek](https://www.slsknet.org/) using metadata from [MusicBrainz](https://musicbrainz.org/) and [Last.fm](https://www.last.fm/).

## Features

* Uses `TagLib`, `eyeD3`, and `metaflac` to tag MP3 and FLAC files.
* Automatically downloads cover art from MusicBrainz and Last.fm.
* Configurable directory and file names.

## Usage

```shell
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
  Scan library and replace mp3 albums with flac versions

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

## Music Library Organization

Djinn assumes that your your music library follows a simple `Artist` / `Album` / `Track` hierarchy.

You should set the `LibraryPath`, `ArtistFormat`, `AlbumFormat`, and `TrackFormat` strings in your configuration file to correspond with the way you organize your music.

For example, given this configuration:

```
"LibraryPath":  "/home/kyle/Music",
"ArtistFormat": "%S",
"AlbumFormat":  "%Y %T",
"TrackFormat":  "%n %t"
```

Djinn would expect your music to be organized as e.g.:

`/home/kyle/Music/Beatles, The/1969 Abbey Road/01 Come Together.flac`

## Configuration

Djinn loads its configuration from `DJINN_CONFIG` or, if that isn't set, from `~/.config/djinn/djinn.json`.

### Configuration File Example

Here is an example of what the configuration file might look like:

```json
{
    "LibraryPath": "/home/kyle/Music",

    "LastFmApiKey": "XXX",
    "LastFmApiSecret": "XXX",

    "SoulseekUsername": "XXX",
    "SoulseekPassword": "XXX",

    "ArtistFormat": "%S",
    "AlbumFormat": "%Y %T",
    "TrackFormat": "%n %t",

    "Watchdog": {
        "TimeoutMinutes": 30,
        "DelaySeconds": 10,
        "MinimumSpeedBytes": 50000,
        "QueuedRemotely": false
    }
}
```

### Format Tokens

The configuration includes format tokens that define how artist, album, and track information should be displayed. The available tokens are as follows:

#### Artist Format Tokens

| Token | Description           | Example      |
| ----- | --------------------- | ------------ |
| `%A`  | Artist Name           | The Beatles  |
| `%S`  | Artist Sort Name      | Beatles, The |
| `%%`  | Literal '%' character | %            |

#### Album Format Tokens

All artist tokens, plus:

| Token | Description | Example   |
| ----- | ----------- | --------- |
| `%T`  | Album Title | Yesterday |
| `%Y`  | Album Year  | 1965      |

#### Track Format Tokens

All artist and album tokens, plus:

| Token | Description                            | Example   |
| ----- | -------------------------------------- | --------- |
| `%t`  | Track Title                            | Yesterday |
| `%n`  | Track Number (formatted as two digits) | 01        |
| `%N`  | Total number of tracks in the album    | 14        |

### Watchdog

TODO

### Viewing Configuration with `djinn config`

You can view the path of the loaded config file and the parsed values by running:

```shell
$ djinn config

Configuration loaded from /home/kyle/.config/djinn/djinn.json
Library path:       /home/kyle/Music
Last.fm API key:    XXX
Last.fm API secret: XXX
Soulseek username:  XXX
Soulseek password:  XXX
...
```

## Source

The source code for Djinn is available on [GitHub](https://github.com/kkestell/djinn).

## License

Djinn uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
