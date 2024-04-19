---
title: XDG Default Applications
subtitle: Fixing broken file associations in Linux.
date: 2021-11-27
draft: false
---

## `xdg-mime`

Print the `.desktop` filename of the application that is registered to open directories:

```shell
xdg-mime query default inode/directory
```

Associate directories with Nautilus (Files). This will modify `~/.config/mimetypes.list`:

```shell
xdg-mime default org.gnome.Nautilus.desktop inode/directory
```

### Example `~/.config/mimeapps.list`

```ini
[Default Applications]
application/json=code.desktop
application/pdf=org.gnome.Evince.desktop
audio/mp3=music.desktop
audio/x-flac=music.desktop
image/jpeg=org.gnome.eog.desktop
image/png=org.gnome.eog.desktop
inode/directory=org.gnome.Nautilus.desktop
text/markdown=org.gnome.TextEditor.desktop
text/plain=org.gnome.TextEditor.desktop
video/mp4=io.github.vlc.desktop
video/ogg=io.github.vlc.desktop
video/quicktime=io.github.vlc.desktop
video/webm=io.github.vlc.desktop
video/x-m4v=io.github.vlc.desktop
video/x-matroska=io.github.vlc.desktop
```

If you want the change to be system-wide, run `xdg-mime` as root. This will modify `/usr/share/applications/mimeapps.list`.

## Further Reading

* [Mozilla Developer Network: Common MIME Types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
* [Arch Wiki: Default Applications](https://wiki.archlinux.org/title/default_applications)