# songfetch
A simple CLI tool, very similar to neofetch, that displays current song information in the terminal.

<img width="1186" height="730" alt="2025-10-17-032127_hyprshot" src="https://github.com/user-attachments/assets/761d714a-932d-4c5b-8065-5f6ae9fcb505" />

<details>
  <summary>More Images</summary>
  <img width="2241" height="1400" alt="2025-10-17-031524_hyprshot" src="https://github.com/user-attachments/assets/32ff2ed2-dce1-47f5-b3f7-9aa397152588" />
<img width="2241" height="1401" alt="2025-10-17-031901_hyprshot" src="https://github.com/user-attachments/assets/adf539ad-9fda-4283-99b5-3c7e7f44a834" />
</details>


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

*Note*: Album art colors will be displayed using ANSI terminal colors and will be affected by custom terminal color schemes (pywal, themes etc.).

This program is designed to be used on **actual songs**, so running this while watching a YouTube video for example, might give unwanted results. This is due to the *non- 1 to 1 aspect ratio* of the "album art" (in this case, a YouTube thumbnail.

## UNINSTALL
- VLC, Spotify, Strawberry, Rhythmbox, Chrome, Brave
