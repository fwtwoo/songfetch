# songfetch
A simple CLI tool, very similar to neofetch, that displays current song information in the terminal.

Notes on the art URL paths:
YTMusic on Firefox: file:///home/fwtwoo/.mozilla/firefox/firefox-mpris/1385_2.png

YouTube of Chrome: file:///tmp/.com.google.Chrome.vAGfHG

Edge (Chromium): file:///tmp/.org.chromium.Chromium.0okaKk

Spotify Desktop App and Web Player (linked): https://i.scdn.co/image/ab67616d0000b273c1a13209dfe146aef3296e34

MPD: No URL (though image exists)

VLC: file:///home/fwtwoo/.cache/vlc/art/artistalbum/Metallica/Kill%20%E2%80%99Em%20All/art.jpg

Rhythmbox: No URL

Strawberry: file:///tmp/strawberry-cover-zqt794.jpg

Lollypop: file:///home/fwtwoo/.cache/lollypop/472c1db1caa9648350644ca0c38b11f0_900_900.jpg

UNINSTALL:
VLC, Spotify, Strawberry, Rhythmbox, Chrome, Brave

## Player Compatibility

### Works Out of the Box ✓

Most players **should** work without any additional setup:
- Spotify, VLC, Firefox, Chrome
- Rhythmbox, Clementine, Strawberry, Audacious
- Any player that supports MPRIS2

Note: The playerctld daemon must be started in order to get proper updates between different players. To start it and set it to run on startup, run:
```bash
systemctl --user enable --now playerctld
```

### Requires Additional Setup

Some terminal/daemon-based players need an MPRIS bridge installed:

| Player | Package to Install | Command |
|--------|-------------------|---------|
| **MPD** | `mpdris2` | `yay -S mpdris2` (Arch)<br>`sudo dnf install mpdris2` (Fedora)<br>`sudo apt install mpdris2` (Debian/Ubuntu)|
| **cmus** | `cmus-mpris` | Check your distro's package manager |
| **moc** | `moc-mpris` | Check your distro's package manager |


After installing the bridge, enable it:
```bash
systemctl --user enable --now mpDris2  # for MPD
# enable similar services for other players
```

