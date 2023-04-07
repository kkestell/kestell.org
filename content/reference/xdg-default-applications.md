---
title: "XDG Default Applications"
description: "Fixing broken file associations in Linux."
created: 2023-03-04
updated: 2023-03-04
---

## `xdg-mime`

Print the `.desktop` filename of the application that is registered to open directories:

```shell
$ xdg-mime query default inode/directory
```

Associate directories with Nautilus (Files). This will modify `~/.config/mimetypes.list`:

```shell
$ xdg-mime default org.gnome.Nautilus.desktop inode/directory
```

### Example `~/.config/mimeapps.list`



```ini
[Default Applications]
audio/x-wav=io.bassi.Amberol.desktop
audio/mp3=io.bassi.Amberol.desktop
audio/ogg=io.bassi.Amberol.desktop
audio/x-flac=io.bassi.Amberol.desktop
application/pdf=org.gnome.Evince.desktop
image/jpeg=org.gnome.eog.desktop
image/png=org.gnome.eog.desktop
inode/directory=org.gnome.Nautilus.desktop
text/plain=org.gnome.TextEditor.desktop
text/markdown=org.gnome.TextEditor.desktop
video/mp4=io.github.celluloid_player.Celluloid.desktop
video/x-matroska=io.github.celluloid_player.Celluloid.desktop
video/webm=io.github.celluloid_player.Celluloid.desktop
video/quicktime=io.github.celluloid_player.Celluloid.desktop
video/x-m4v=io.github.celluloid_player.Celluloid.desktop
video/ogg=io.github.celluloid_player.Celluloid.desktop
```

If you want the change to be system-wide, run `xdg-mime` as root. This will modify `/usr/share/applications/mimeapps.list`.

## Further Reading

* [Mozilla Developer Network: Common MIME Types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
* [Arch Wiki: Default Applications](https://wiki.archlinux.org/title/default_applications)