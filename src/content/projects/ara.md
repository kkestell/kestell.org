---
title: "Ara"
subtitle: "An imperative, statically typed programming language."
date: 2023-04-02
draft: false
---

## Implementation

### Parsing

The Ara compiler uses a hand-written LL(1) recursive descent parser that uses a single token lookahead to make parsing decisions without the need for backtracking.

### Code Generation

The Ara compiler emits LLVM IR.

## Source

The source code for Ara is available on [GitHub](https://github.com/kkestell/ara).

## License

Ara uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.