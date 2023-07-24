---
title: "Archive"
subtitle: "Back up important files to an SSD."
date: 2023-07-24
draft: false
---

This is just an old Samsung EVO 850 SSD connected to a Raspberry Pi using a USB to SATA adapter, and a shell script that's run on a Systemd timer. The network share is mounted read-only, and the script uses `rsync` to copy files from the network share to the SSD.

## Source

The source code for Archive is available on [GitHub](https://github.com/kkestell/archive).

## License

Archive uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.