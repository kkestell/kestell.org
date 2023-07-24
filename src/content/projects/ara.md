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

## Example

```
fn fib(n: int): int
{
    if (n == 0)
    {
        return 0
    }

    if (n == 1)
    {
        return 1
    }
  
    return fib(n-2) + fib(n-1)
}

fn main(): int
{
    return fib(10)
}
```

## Source

The source code for Ara is available on [GitHub](https://github.com/kkestell/ara).

## License

Ara uses the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).