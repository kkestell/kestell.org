---
title: "Z-Probe Offset"
date: 2023-01-15T05:57:00-06:00
draft: false
---

| GCode | Description |      |
| ----- | ----------- | ---- |
| `M851 Z0` | Set Z-probe offset to 0. | [?](https://marlinfw.org/docs/gcode/M851.html) |
| `M500` | Save all configurable settings to EEPROM. | [?](https://marlinfw.org/docs/gcode/M500.html) |
| `M501` | Load all saved settings from EEPROM. | [?](https://marlinfw.org/docs/gcode/M501.html) |
| `M503` | Print all runtime-configurable settings to the host console. | [?](https://marlinfw.org/docs/gcode/M503.html) |
| `G28` | Auto home. | [?](https://marlinfw.org/docs/gcode/G028.html) |
| `G1 F60 Z0` | Move to Z0. | [?](https://marlinfw.org/docs/gcode/G000-G001.html) |
| `M211 S0` | Unlock software endstops to enable movement below Z0. | [?](https://marlinfw.org/docs/gcode/M211.html) |
| `M109 S190` | Set nozzle temperature to 220 °C. | [?](https://marlinfw.org/docs/gcode/M109.html) |
| `G1 F60 Z-0.2` | Move extruder to Z-0.2. Adjust the value in the previous step until you can just barely move a piece of paper placed between the nozzle and print bed. Subtract another 0.1 from this value. This will be your new Z-probe offset value. | [?](https://marlinfw.org/docs/gcode/G000-G001.html) |
| `M851 Z-2.2` | Set Z-probe offset to -2.2. This value should be whatever you measured in the previous step. | [?](https://marlinfw.org/docs/gcode/M851.html) |
| `M211 S0` | Lock software endstops to prevent movement below Z0. | [?](https://marlinfw.org/docs/gcode/M211.html) |
| `M500` | Save all configurable settings to EEPROM. | [?](https://marlinfw.org/docs/gcode/M500.html) |
| `M501` | Load all saved settings from EEPROM. | [?](https://marlinfw.org/docs/gcode/M501.html) |
| `M503` | Print all runtime-configurable settings to the host console. | [?](https://marlinfw.org/docs/gcode/M503.html) |
| `G28` | Auto home. | [?](https://marlinfw.org/docs/gcode/G028.html) |
| `G1 F60 Z0` | Move to Z0 to confirm. | [?](https://marlinfw.org/docs/gcode/G000-G001.html) |
| `M109 S0` | Set nozzle temperature to 0 °C. | [?](https://marlinfw.org/docs/gcode/M109.html) |

<!--
---


No, it is not necessary to call G29 before every print to "auto level the bed" 1) provided that:

the bed surface has not changed (e.g. large load or force has been exerted on the build platform, leveling screws are accidentally adjusted, a substantial different bed temperature is used causing different thermal stresses, etc.),
the carriage of the hotend is stable (some printers, e.g. the cantilever type, or single side Z lead screw driven printers are more prone to an unstable or level axis), and
the scanned surface geometry is saved in the controller board memory.
There are several solutions to solve this. You could manually run the G29 command once in a while storing the scanned surface with an M500 command to save the mesh to the EEPROM (memory) of the controller board (this can be done from the printer controller display for Marlin operated printers, an interface like a terminal or a print server application, or from pre-stored .g/G-code files on an SD card). If you use the SD-card, note that it is possible to auto-launch G-code files from the root of the SD-card upon inserting.

Do note to remove the G29 command in the start code of the slicer. The G29 command needs to be replaced with M420 S1 for Marlin firmware operated printers. This command will load the saved mesh at the start of the print from memory. This is especially useful when using a large amount of probing points (e.g. a large bed mesh using a 10 x 10 mesh of 100 probing points, to ensure the mesh is up-to-date, once in a while initiate the scanning sequence to store an updated mesh).

1) Please note that auto-bed leveling might be confusingly indicating that some magic leveling of the build platform/surface itself is taking place (this is also possible in Marlin when there are multiple Z steppers and lead screws used), but, that is not actually what is meant with this phrasing. The process of the auto-bed leveling actually scans the surface of the build surface and compensates the height of the print head/nozzle during a predefined printing height (usually 10 mm, set in the firmware or through G-code: M420 Z10 ; Gradually reduce compensation until Z=10), during this printing process the nozzle gradually be less and less compensated until there is no compensation and the print nozzle will print parallel to the guide axis (e.g. the X-axis in i3 style printers and X-Y axes in CoreXY kinematics printers.
-->