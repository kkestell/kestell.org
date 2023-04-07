---
title: "TRS-80 Model 100"
description: "Lorem ipsum dolor sit amet"
created: 2021-11-27
updated: 2022-04-14
---

## Overview

TODO

![TRS-80 Model 100](/static/images/trs-80.jpg)

TODO

## Screen

### LCD

The display has a 192×480 IPS panel. I think I read somewhere that these were designed as rear-view mirrors. At 218mm, it's actually a little wider than the original LCD.

### Bracket

The LCD is mounted to a custom 3D printed bracket that's attached to the enclosure using the original screw bosses. The LCD fits snugly between bracket and the front plastic, with three pieces of double sided tape between the display and the bracket for good measure.

{{< model src="lcd-bracket.obj" >}}

### Configuration

```ini
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_force_mode=1
hdmi_timings=480 0 30 30 30 1920 0 6 6 6 0 0 0 60 0 66000000 7
max_framebuffer_width=480
max_framebuffer_height=1920
display_hdmi_rotate=1
```

## Keyboard

### Matrix

TODO

![TRS-80 Model 100 Keyboard Matrix](/static/images/keyboard-matrix.jpg)