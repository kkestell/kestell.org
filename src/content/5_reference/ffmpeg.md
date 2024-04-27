---
title: FFmpeg
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

Record RTSP stream w/ hardware acceleration (NVIDIA):

```bash
ffmpeg -rtsp_transport tcp -i rtsp://10.0.0.1/ -c:v h264_nvenc -preset fast -b:v 1000k -c:a copy output.mp4
```
