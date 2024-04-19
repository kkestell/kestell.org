---
title: BdfNet
subtitle: .NET library for loading Glyph Bitmap Distribution Format (BDF) fonts.
date: 2023-12-11
draft: false
---

BdfNet is a .NET library for loading [Glyph Bitmap Distribution Format](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format) (BDF) fonts.

## Example

```csharp
var font = BdfFont.Load("courR14.bdf");
var aChar = font.Characters[0x61];

for (var row = 0; row < aChar.Height; row++)
{
    for (var col = 0; col < aChar.Width; col++)
    {
        Console.Write(aChar.Bitmap[row, col] == 1 ? "*" : " ");
    }
    Console.WriteLine();
}
```

### Output

```
  ***  
 *   * 
     * 
 ***** 
*    * 
*    * 
 **** *

```

## Source

The source code for BdfNet is available on [GitHub](https://github.com/kkestell/bdfnet).

## License

BdfNet uses the [Zero-Clause BSD](https://opensource.org/license/0bsd/) license.
