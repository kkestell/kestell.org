---
title: "Nonsense"
date: 2023-03-04T05:56:00-06:00
draft: false
---

## Linux

### File Associations

#### Directories are not opened in the file manager

You may find that an application that is not a file manager, Audacious or Visual Studio Code for example, is set as the default application for opening directories — an application that specifies that it can handle the `inode/directory` MIME type in its desktop entry can become the default. You can query the default application for opening directories with the following command:

```
$ xdg-mime query default inode/directory
```

To ensure that directories are opened in the file manager, run the following command:

```
$ xdg-mime default org.gnome.Nautilus.desktop inode/directory
```

where `org.gnome.Nautilus.desktop` is the desktop entry for your file manager.

If you want the change to be system-wide, run the command above as root or create/edit the following file:

`/usr/share/applications/mimeapps.list`:

```
[Default Applications]
inode/directory=my_file_manager.desktop
```

See: https://wiki.archlinux.org/title/default_applications