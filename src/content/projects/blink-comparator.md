---
title: "Blink Comparator"
description: ""
date: 2019-12-01
draft: false
---

## Overview

`blink-comparator` is a Python program that periodically fetches a website and compares the current version with the previous one. If the two versions are different, a Telegram message is sent to the user that contains a diff of the two versions.

To date, I've used this program to find:

* COVID vaccine appointments in my area
* Stock availability of infant formula, mason jars, and other items
* Early childhood family education class openings

Blink Comparator was designed to consume minimal system resources -- I have it running on a Raspberry Pi -- and to be as simple and foolproof as possible.

## The Name

> A blink comparator is a viewing apparatus formerly used by astronomers to find differences between two photographs of the night sky. It permits rapid switching from viewing one photograph to viewing the other, "blinking" back and forth between the two images taken of the same area of the sky at different times. This allows the user to more easily spot objects in the night sky that have changed position or brightness.

![Blink Comparator](/static/images/blink-comparator.gif)

See: https://en.wikipedia.org/wiki/Blink_comparator

## Source

The source code for Blink Comparator is available on [GitHub](https://github.com/kkestell/blink-comparator).

## License

Blink Comparator uses the [Unlicense](https://unlicense.org/).