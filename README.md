# songfetch
A simple CLI tool, very similar to neofetch, that displays current song information in the terminal.

## Player Compatibility

### Works Out of the Box ✓

Most players **should** work without any additional setup:
- Spotify, VLC, Firefox, Chrome
- Rhythmbox, Clementine, Strawberry
- Any player that supports MPRIS2

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

**Note:** The `playerctld` daemon must be started in order to get proper updates between different players. To start it and set it to run on startup, run:
```bash
systemctl --user enable --now playerctld
```

If you get an error like `Unit playerctld.service does not exist`, or issues with player instances not updating correctly, create a user systemd service:

Create `~/.config/systemd/user/playerctld.service`:
```
[Unit]
Description=playerctld daemon

[Service]
ExecStart=/usr/bin/playerctld daemon

[Install]
WantedBy=default.target
```

Reload user systemd and enable with:
```bash
systemctl --user daemon-reload
systemctl --user enable --now playerctld
```

If you see `playerctld DBus service is already running`, it means another instance is active. Kill it with:
```bash
pkill playerctld
```
Then restart the systemd service as above.

Note: Album art colors use ANSI terminal colors and will be affected by custom terminal color schemes (pywal, etc.)

## UNINSTALL
- VLC, Spotify, Strawberry, Rhythmbox, Chrome, Brave
