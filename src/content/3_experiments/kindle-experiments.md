---
title: Kindle Experiments
date: 2024-03-07
draft: false
---

## SSH

See: [MobileRead Wiki - USBNetwork](https://wiki.mobileread.com/wiki/USBNetwork)

Enable USBNetwork, connect the Kindle to your computer via USB, and configure the network interface thusly:

IP
:   192.168.15.201

Netmask
:   255.255.255.0

Then connect to the Kindle via SSH (no password):

```
ssh root@192.168.15.244
```

## Search Bar Commands

See: [What commands can be given in the Kindle's search box?](https://ebooks.stackexchange.com/questions/152/what-commands-can-be-given-in-the-kindles-search-box)

| Command | Description      |
| ------- | ---------------- |
| `;711`  | WiFi information |
