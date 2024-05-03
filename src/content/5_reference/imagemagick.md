---
title: ImageMagick
date: 2024-05-03
draft: false
---

Trim transparent pixels from an image:

```bash
convert input.png -fuzz 0% -trim +repage output.png
```