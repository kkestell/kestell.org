---
title: Brother HL L2340D Laser Printer
date: 2024-05-03
draft: false
---

## Setup

### Install CUPS and Drivers

```
yay -Sy cups cups-pdf brlaser
```

### Enable and Start Services

```
sudo systemctl enable cups.socket
sudo systemctl enable cups.service
sudo systemctl start cups.socket
```

### Add Printer

Search for `ipp://BRW1008B16E541A.lan:631/ipp` and select the LPD option.

![Add Printer 1](/static/images/add-printer-1.png)

Select "Brother HL-L2340D series, using brlaser v6".

![Add Printer 2](/static/images/add-printer-2.png)
