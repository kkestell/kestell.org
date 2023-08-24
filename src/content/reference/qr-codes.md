---
title: "Generating QR Codes"
subtitle: ""
date: 2021-11-27
draft: false
---

![QR Code](/static/images/qr.png)

## `qrencode`

### WiFi QR Codes

Replace `ssid` and `password` with the appropriate values.

```shell
qrencode -o qr.png "WIFI:T:WPA;S:ssid;P:password;;"
```

### URLs

```shell
qrencode -o qr.png "https://example.com"
```

### Printing

I have a Brother HL-L2300D laser printer which has a native print resolution of 600 DPI. I'd like to be able to print my QR code on a standard US letter-size piece of paper. According to [the manual](https://support.brother.com/g/s/id/htmldoc/printer/cv_hll2300d/use/manual/index.html#GUID-1BBF837B-7708-4FCB-8F03-EBC668571B9F_20#KEY=unprintable%20areas), the minimum margins on the Brother HL-L2300D are 0.16", so I figure an 8" QR code gives me 0.25" of margin, which[^1] is plenty. Dividied by 25, that's 192 pixels per dot.

Generate the QR code:

```shell
qrencode -o qr.png -s 192 -m 0 -d 600 "whatever"
```

`-s`
:   Size of each dot in pixels

`-m`
:   Margin in dots

`-d`
:   DPI

`-o`
:   Output file

And print it:

```shell
lpr qr.png
```
   
[^1]: I have a Brother HL-L2300D laser printer1 which has a native print resolution of 600 DPI. I'd like to be able to print my QR code on a standard US letter-size piece of paper. According to the manual, the minimum margins on the Brother HL-L2300D are 0.16", so I figure an 8" QR code gives me
