---
title: find
date: 2024-05-12
draft: false
---

Delete files that don't have a `.pdf` extension:

```bash
find . -type f ! -name '*.pdf' -delete
```

Delete empty directories:

```bash
find . -type d -empty -delete
```
