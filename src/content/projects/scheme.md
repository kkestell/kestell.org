---
title: "Scheme"
subtitle: "Scheme interpreter."
date: 2023-05-29
draft: false
---

## Example

```scheme
(define factorial
    (lambda (n)
        (if (= n 0)
            1
            (* n (factorial (- n 1)))
        )
    )
)

(define print-factorials-up-to
    (lambda (n)
        (let ((i 1))
            (while (<= i n)
                (begin
                    (display "Factorial of ")
                    (display i)
                    (display " is ")
                    (display (factorial i))
                    (newline)
                    (set! i (+ i 1))
                )
            )
        )
    )
)

(print-factorials-up-to 10)
```

## Source

The source code for Scheme is available on [GitHub](https://github.com/kkestell/scheme).

## License

Scheme uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
