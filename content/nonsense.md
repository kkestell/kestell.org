---
title: "Nonsense"
description: "Nonsense nonsense nonsense"
created: 2023-03-04
updated: 2023-03-04
---

## Linux

### File Associations

#### Directories are not opened in the file manager

You may find that an application that is not a file manager, Audacious or Visual Studio Code for example, is set as the default application for opening directories — an application that specifies that it can handle the `inode/directory` MIME type in its desktop entry can become the default. You can query the default application for opening directories with the following command:

```shell
$ xdg-mime query default inode/directory
```

To ensure that directories are opened in the file manager, run the following command:

```shell
$ xdg-mime default org.gnome.Nautilus.desktop inode/directory
```

where `org.gnome.Nautilus.desktop` is the desktop entry for your file manager.

Or maybe Ultimaker Cura decided it was your new image viewer:

```shell
$ xdg-mime default org.gnome.eog.desktop image/jpeg image/png
```

The `xdg-mime default` command will modify `~/.config/mimetypes.list`.

If you want the change to be system-wide, run the command above as root. This will modify`/usr/share/applications/mimeapps.list`.

```ini
[Default Applications]
inode/directory=my_file_manager.desktop
```

See: [https://wiki.archlinux.org/title/default_applications](https://wiki.archlinux.org/title/default_applications)