# songfetch
A simple CLI tool, very similar to neofetch, that displays current song information in the terminal.

Notes:
YTMusic on Firefox: 

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

