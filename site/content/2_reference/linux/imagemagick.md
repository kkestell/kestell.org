---
title: ImageMagick
date: 2024-05-03
draft: false
---

Trim transparent pixels from an image:

```bash
convert input.png -fuzz 0% -trim +repage output.png
```

Convert PDF to JPG:

```bash
convert -density 70 -quality 100 -flatten input.pdf output.jpg
```
Add drop shadow:

NOTE: `20x4+0+0` is 20% opacity, 4px sigma (blur amount), 0 horizontal offset, 0 vertical offset.

```bash
convert input.jpg \( +clone -background black -shadow 20x4+0+0 \) +swap -background none -layers merge +repage output.png
```
