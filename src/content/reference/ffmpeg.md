---
title: "FFmpeg"
subtitle: ""
date: 2023-08-21
draft: false
---

Change video speed (2.0x):

```bash
ffmpeg -i input.mkv -vf "setpts=(PTS-STARTPTS)/2.0" -af atempo=2.0 output.mkv
```

Change container from MKV to MP4:

```bash
ffmpeg -i input.mkv -codec copy output.mp4
```
