---
title: "Z-Probe Offset"
description: Z-offset calibration procedure for Marlin firmware.
created: 2023-01-15
updated: 2023-01-15
---

| GCode        | Description                                                                                                                                                                                                                              |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M851 Z0      | Set Z-probe offset to 0.                                                                                                                                                                                                                 |
| M500         | Save all configurable settings to EEPROM.                                                                                                                                                                                                |
| M501         | Load all saved settings from EEPROM.                                                                                                                                                                                                     |
| M503         | Print all runtime-configurable settings to the host console.                                                                                                                                                                             |
| G28          | Auto home.                                                                                                                                                                                                                               |
| G1 F60 Z0    | Move to Z0.                                                                                                                                                                                                                              |
| M211 S0      | Unlock software endstops to enable movement below Z0.                                                                                                                                                                                    |
| M109 S190    | Set nozzle temperature to 220 °C.                                                                                                                                                                                                        |
| G1 F60 Z-0.2 | Move extruder to Z-0.2. Adjust the value in the previous step until you can just barely move a piece of paper placed between the nozzle and print bed. Subtract another 0.1 from this value. This will be your new Z-probe offset value. |
| M851 Z-2.2   | Set Z-probe offset to -2.2. This value should be whatever you measured in the previous step.                                                                                                                                             |
| M211 S0      | Lock software endstops to prevent movement below Z0.                                                                                                                                                                                     |
| M500         | Save all configurable settings to EEPROM.                                                                                                                                                                                                |
| M501         | Load all saved settings from EEPROM.                                                                                                                                                                                                     |
| M503         | Print all runtime-configurable settings to the host console.                                                                                                                                                                             |
| G28          | Auto home.                                                                                                                                                                                                                               |
| G1 F60 Z0    | Move to Z0 to confirm.                                                                                                                                                                                                                   |
| M109 S0      | Set nozzle temperature to 0 °C.                                                                                                                                                                                                          |

## `start.gcode`

```gcode
; Set Heat Bed temperature
M140 S{material_bed_temperature_layer_0}

; Set Extruder temperature
M104 S{material_print_temperature_layer_0}

; Home all axes
G28

; Level bed
G29

; Reset Extruder
G92 E0

; Move to start position
G1 X0.1 Y20 Z0.3 F5000.0

; Wait for Heat Bed temperature
M190 S{material_bed_temperature_layer_0}

; Wait for Extruder temperature
M109 S{material_print_temperature_layer_0}

; Draw the first line
G1 X5.5 Y200.0 Z0.3 F1500.0 E15

; Move to side a little
G1 X5.9 Y200.0 Z0.3 F5000.0

; Draw the second line
G1 X5.9 Y20 Z0.3 F1500.0 E30

; Reset Extruder
G92 E0

; Move Z Axis up little to prevent scratching of Heat Bed
G1 Z2.0 F3000
```

## `end.gcode`

```gcode
; Relative positioning
G91

; Retract
G1 E-2 F2700

; Retract and raise Z
G1 E-2 Z0.2 F2400

; Wipe out
G1 X5 Y5 F3000

; Raise Z more
G1 Z10

; Absolute positionning
G90

; Present
G1 X0 Y{machine_depth}

; Turn-off fan
M106 S0

; Turn-off hotend
M104 S0 

; Turn-off bed 
M140 S0

; Disable all steppers but Z
M84 X Y E
```

<!--
No, it is not necessary to call G29 before every print to "auto level the bed" 1) provided that:

the bed surface has not changed (e.g. large load or force has been exerted on the build platform, leveling screws are accidentally adjusted, a substantial different bed temperature is used causing different thermal stresses, etc.),
the carriage of the hotend is stable (some printers, e.g. the cantilever type, or single side Z lead screw driven printers are more prone to an unstable or level axis), and
the scanned surface geometry is saved in the controller board memory.
There are several solutions to solve this. You could manually run the G29 command once in a while storing the scanned surface with an M500 command to save the mesh to the EEPROM (memory) of the controller board (this can be done from the printer controller display for Marlin operated printers, an interface like a terminal or a print server application, or from pre-stored .g/G-code files on an SD card). If you use the SD-card, note that it is possible to auto-launch G-code files from the root of the SD-card upon inserting.

Do note to remove the G29 command in the start code of the slicer. The G29 command needs to be replaced with M420 S1 for Marlin firmware operated printers. This command will load the saved mesh at the start of the print from memory. This is especially useful when using a large amount of probing points (e.g. a large bed mesh using a 10 x 10 mesh of 100 probing points, to ensure the mesh is up-to-date, once in a while initiate the scanning sequence to store an updated mesh).

1) Please note that auto-bed leveling might be confusingly indicating that some magic leveling of the build platform/surface itself is taking place (this is also possible in Marlin when there are multiple Z steppers and lead screws used), but, that is not actually what is meant with this phrasing. The process of the auto-bed leveling actually scans the surface of the build surface and compensates the height of the print head/nozzle during a predefined printing height (usually 10 mm, set in the firmware or through G-code: M420 Z10 ; Gradually reduce compensation until Z=10), during this printing process the nozzle gradually be less and less compensated until there is no compensation and the print nozzle will print parallel to the guide axis (e.g. the X-axis in i3 style printers and X-Y axes in CoreXY kinematics printers.
-->