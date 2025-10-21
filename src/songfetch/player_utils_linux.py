import subprocess, getpass, re

# Default values for fallback
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

# We'll need users audio backend (pipewire, pulse, etc.)
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

# Now we get some MPRIS info
def get_player_name():
    # Get the current player
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ playerName }}"
        ], capture_output=True, text=True)
        name = result.stdout.strip()
        return name if name else DEFAULTS["player_name"]
    except Exception:
        return DEFAULTS["player_name"]

def get_art():
    # Get the current album art
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ mpris:artUrl }}"
        ], capture_output=True, text=True)
        art = result.stdout.strip()
        return art if art else DEFAULTS["art"]
    except Exception:
        return DEFAULTS["art"]

def get_title():
    # Get the artist
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ trunc(title, 33) }}"
        ], capture_output=True, text=True)
        title = result.stdout.strip()
        return title if title else DEFAULTS["title"]
    except Exception:
        return DEFAULTS["title"]

def get_artist():
    # Get the artist
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ trunc(artist, 32) }}"
        ], capture_output=True, text=True)
        artist = result.stdout.strip()
        return artist if artist else DEFAULTS["artist"]
    except Exception:
        return DEFAULTS["artist"]

def get_album():
    # Get the album
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ trunc(album, 33) }}"
        ], capture_output=True, text=True)
        album = result.stdout.strip()
        return album if album else DEFAULTS["album"]
    except Exception:
        return DEFAULTS["album"]

def get_duration_formatted():
    # Get the album
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ duration(mpris:length) }}"
        ], capture_output=True, text=True)
        duration = result.stdout.strip()
        return duration if duration else DEFAULTS["duration_formatted"]
    except Exception:
        return DEFAULTS["duration_formatted"]

# Now we need to get current volume
def get_volume():
    # Use backend function
    try:
        current_backend = get_backend()
        # Check all major backends
        if current_backend == "PipeWire":
            # Most common modern backend
            result = subprocess.run([
                "wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"
            ], capture_output=True, text=True)
            # Regex to only include the decimal digit
            final_result = re.search(r'\d+\.\d+', result.stdout)
            # Very hacky convertion but works for now xD
            percentage = int(float(final_result.group()) * 100) if final_result else DEFAULTS["volume"]
        elif current_backend == "PulseAudio":
            # Older systems
            result = subprocess.run([
                "pactl", "get-sink-volume", "@DEFAULT_SINK@"
            ], capture_output=True, text=True)
            # Regex to only include the percentage value
            final_result = re.search(r'(\d+)%', result.stdout)
            percentage = int(final_result.group()) if final_result else DEFAULTS["volume"]
        else:
            # Most likely ALSA
            result = subprocess.run([
                "amixer", "get", "Master"
            ], capture_output=True, text=True)
            # Similar regex to pulseaudio
            final_result = re.search(r'(\d+)%', result.stdout)
            percentage = int(final_result.group()) if final_result else DEFAULTS["volume"]
        return f"{percentage}%" if isinstance(percentage, int) else DEFAULTS["volume"]
    except Exception:
        return DEFAULTS["volume"]

def get_position():
    # Getting the info from playerctl
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ position }}"
        ], capture_output=True, text=True)
        pos = result.stdout.strip()
        return int(pos) if pos.isdigit() else DEFAULTS["position"]
    except Exception:
        return DEFAULTS["position"]

def get_duration():
    # Getting the info from playerctl
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ mpris:length }}"
        ], capture_output=True, text=True)
        dur = result.stdout.strip()
        return int(dur) if dur.isdigit() else DEFAULTS["duration"]
    except Exception:
        return DEFAULTS["duration"]

def get_url():
    # Getting the info from playerctl
    try:
        result = subprocess.run([
            "playerctl", "metadata", "--format", "{{ trunc(xesam:url, 35) }}"
        ], capture_output=True, text=True)
        url = result.stdout.strip()
        return url if url else DEFAULTS["url"]
    except Exception:
        return DEFAULTS["url"]

def get_status():
    # Getting the rest of the info
    try:
        result = subprocess.run([
            "playerctl", "status"
        ], capture_output=True, text=True)
        status = result.stdout.strip()
        return status if status else DEFAULTS["status"]
    except Exception:
        return DEFAULTS["status"]

def get_loop():
    # Getting the rest of the info
    try:
        result = subprocess.run([
            "playerctl", "loop"
        ], capture_output=True, text=True)
        loop = result.stdout.strip()
        return loop if loop else DEFAULTS["loop"]
    except Exception:
        return DEFAULTS["loop"]

def get_shuffle():
    # Getting the rest of the info
    try:
        result = subprocess.run([
            "playerctl", "shuffle"
        ], capture_output=True, text=True)
        shuffle = result.stdout.strip()
        return shuffle if shuffle else DEFAULTS["shuffle"]
    except Exception:
        return DEFAULTS["shuffle"]

def get_user():
    try:
        username = getpass.getuser()
        return username if username else DEFAULTS["user"]
    except Exception:
        return DEFAULTS["user"]
