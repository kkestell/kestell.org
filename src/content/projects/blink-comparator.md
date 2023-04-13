---
title: "Blink Comparator"
description: ""
date: 2019-12-01
draft: false
---

## Overview

`blink-comparator` periodically fetches a website and compares the current version with what it fetched previously. If it detects any differences, it sends a Telegram message containing a diff of the two versions to the user.

So far, I have used this program to:

* Locate COVID vaccine appointments in my area
* Check stock availability for infant formula, mason jars, and other items
* Find openings in early childhood family education classes

Blink Comparator is designed to consume minimal system resources and to be as simple and foolproof as possible.

## The Name

> A blink comparator is a viewing apparatus formerly used by astronomers to find differences between two photographs of the night sky. It permits rapid switching from viewing one photograph to viewing the other, "blinking" back and forth between the two images taken of the same area of the sky at different times. This allows the user to more easily spot objects in the night sky that have changed position or brightness.

![Blink Comparator](/static/images/blink-comparator.gif)

See: https://en.wikipedia.org/wiki/Blink_comparator

## Source

The source code for Blink Comparator is available on [GitHub](https://github.com/kkestell/blink-comparator).

## License

Blink Comparator uses the [Unlicense](https://unlicense.org/).