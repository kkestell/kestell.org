---
title: Parallel SSH
subtitle: Run commands on multiple SSH hosts in parallel.
date: 2023-05-29
draft: false
---

pssh is a C# program for executing a specified command on multiple SSH hosts in parallel. The command output and error messages are displayed on the console with a unique color for each host.

I mainly use this to keep my Raspberry Pis up to date. For example:

```
pssh "sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get upgrade -y"
```

## Source

The source code for Parallel SSH is available on [GitHub](https://github.com/kkestell/pssh).

## License

Parallel SSH uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
