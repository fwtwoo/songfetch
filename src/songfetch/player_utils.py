#!/usr/bin/env python3
import dbus, getpass, re
from math import floor
from datetime import timedelta

DEFAULTS = {
    "player_name": "No player",
    "art": "",
    "title": "No title found",
    "artist": "No artist found",
    "album": "No album found",
    "duration_formatted": "00:00",
    "volume": "Unknown",
    "position": 0,
    "duration": 0,
    "url": "No URL found",
    "status": "No status",
    "loop": "Unknown",
    "shuffle": "Unknown",
    "user": "No User"
}

import subprocess
def get_backend():
    try:
        if subprocess.run(["pgrep", "-x", "pipewire"], capture_output=True, text=True).returncode == 0:
            return "PipeWire"
        elif subprocess.run(["pgrep", "-x", "pulseaudio"], capture_output=True, text=True).returncode == 0:
            return "PulseAudio"
        else:
            return "ALSA"
    except Exception:
        return "Unknown"

def to_python(obj):
    # recursive convert dbus types -> python primitives
    if isinstance(obj, dbus.Array):
        return [to_python(x) for x in obj]
    if isinstance(obj, dbus.Dictionary):
        return {to_python(k): to_python(v) for k, v in obj.items()}
    if isinstance(obj, (dbus.String, dbus.ObjectPath)):
        return str(obj)
    if isinstance(obj, (dbus.Int64, dbus.Int32, dbus.Double)):
        return float(obj)
    if isinstance(obj, (dbus.Boolean,)):
        return bool(obj)
    return obj

def get_player_props():
    try:
        bus = dbus.SessionBus()
        player = bus.get_object('org.mpris.MediaPlayer2.playerctld', '/org/mpris/MediaPlayer2')
        props = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
        return props
    except Exception:
        return None

def format_duration_seconds(sec):
    try:
        sec = int(round(sec))
        if sec < 0:
            return DEFAULTS["duration_formatted"]
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
    except Exception:
        return DEFAULTS["duration_formatted"]

def get_metadata_raw():
    props = get_player_props()
    if not props:
        return {}
    try:
        md = props.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
        return to_python(md)
    except Exception:
        return {}

def get_player_name():
    # playerctld doesn't provide separate playerName property; keep previous fallback
    # try 'xesam:service' in metadata or use default name
    md = get_metadata_raw()
    name = md.get('kde:playerName') or md.get('xesam:service') or DEFAULTS["player_name"]
    return name

def get_art():
    md = get_metadata_raw()
    return md.get('mpris:artUrl') or DEFAULTS["art"]

def get_title():
    md = get_metadata_raw()
    title = md.get('xesam:title') or DEFAULTS["title"]
    return (title if len(title) <= 33 else title[:30] + '...')

def get_artist():
    md = get_metadata_raw()
    artists = md.get('xesam:artist') or []
    if isinstance(artists, list):
        artist = ", ".join([a for a in artists if a])
    else:
        artist = str(artists)
    artist = artist.strip() or DEFAULTS["artist"]
    return (artist if len(artist) <= 32 else artist[:29] + '...')

def get_album():
    md = get_metadata_raw()
    album = md.get('xesam:album') or DEFAULTS["album"]
    return (album if len(album) <= 33 else album[:30] + '...')

def get_duration_formatted():
    dur = get_duration()
    return format_duration_seconds(dur)

def get_volume():
    props = get_player_props()
    if not props:
        return DEFAULTS["volume"]
    try:
        vol = props.Get('org.mpris.MediaPlayer2.Player', 'Volume')
        vol = float(vol)  # MPRIS Volume is 0.0-1.0 usually (some players use raw)
        perc = int(round(vol * 100)) if 0 <= vol <= 1 else int(round(vol))
        return f"{perc}%"
    except Exception:
        return DEFAULTS["volume"]

def get_position():
    props = get_player_props()
    if not props:
        return DEFAULTS["position"]
    try:
        pos = props.Get('org.mpris.MediaPlayer2.Player', 'Position')
        # Position is microseconds
        return int(pos / 1_000_000)
    except Exception:
        return DEFAULTS["position"]

def get_duration():
    md = get_metadata_raw()
    # mpris:length is microseconds
    try:
        length = md.get('mpris:length') or 0
        return int(length / 1_000_000)
    except Exception:
        return DEFAULTS["duration"]

def get_url():
    md = get_metadata_raw()
    return md.get('xesam:url') or md.get('kde:mediaSrc') or DEFAULTS["url"]

def get_status():
    props = get_player_props()
    if not props:
        return DEFAULTS["status"]
    try:
        return props.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus') or DEFAULTS["status"]
    except Exception:
        return DEFAULTS["status"]

def get_loop():
    props = get_player_props()
    if not props:
        return DEFAULTS["loop"]
    try:
        return props.Get('org.mpris.MediaPlayer2.Player', 'LoopStatus') or DEFAULTS["loop"]
    except Exception:
        return DEFAULTS["loop"]

def get_shuffle():
    props = get_player_props()
    if not props:
        return DEFAULTS["shuffle"]
    try:
        sh = props.Get('org.mpris.MediaPlayer2.Player', 'Shuffle')
        return "On" if sh else "Off"
    except Exception:
        return DEFAULTS["shuffle"]

def get_user():
    try:
        return getpass.getuser() or DEFAULTS["user"]
    except Exception:
        return DEFAULTS["user"]

# Example usage
if __name__ == "__main__":
    print({
        "player_name": get_player_name(),
        "title": get_title(),
        "artist": get_artist(),
        "album": get_album(),
        "art": get_art(),
        "position": get_position(),
        "duration": get_duration(),
        "duration_formatted": get_duration_formatted(),
        "volume": get_volume(),
        "url": get_url(),
        "status": get_status(),
        "loop": get_loop(),
        "shuffle": get_shuffle(),
        "user": get_user()
    })
