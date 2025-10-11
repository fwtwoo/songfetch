import subprocess, getpass, re

# We'll need users audio backend (pipewire, pulse, etc.)
def get_backend():
    if subprocess.run(["pgrep", "-x" "pipewire"], capture_output = True, text = True):
        return "PipeWire"
    elif subprocess.run(["pgrep", "-x" "pulseaudio"], capture_output = True, text = True):
        return "PulseAudio"
    else:
        return "ALSA"

# Now we get some MPRIS info
def get_player_name():
    # Get the current player
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ playerName }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_art():
    # Get the current album art
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ mpris:artUrl }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_title():
    # Get the artist
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ title }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_artist():
    # Get the artist
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ artist }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_album():
    # Get the album
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ album }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_duration_formatted():
    # Get the album
    result = subprocess.run([
        "playerctl", "metadata", "--format", "{{ duration(mpris:length) }}"
    ], capture_output = True, text = True)

    return result.stdout.strip()

# Now we need to get current volume
def get_volume():
    # Use backend function
    current_backend = get_backend()

    # Check all major backends
    if current_backend == "PipeWire":
        # Most common modern backend
        result = subprocess.run([
            "wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"
        ], capture_output = True, text = True)

        # Regex to only include the decimal digit
        final_result = re.search(r'\d+\.\d+', result.stdout)
        # Very hacky convertion but works for now xD
        percentage = int(float(final_result.group()) * 100)

    elif current_backend == "PulseAudio":
        # Older systems
        result = subprocess.run([
            "pactl", "get-sink-volume", "@DEFAULT_SINK@"
        ], capture_output = True, text = True)

        # Regex to only include the percentage value
        final_result = re.search(r'(\d+)%', result.stdout)
        percentage = int(float(final_result.group()))

    else:
        # Most likely ALSA
        result = subprocess.run([
            "amixer", "get", "Master"
        ], capture_output = True, text = True)

        # Similar regex to pulseaudio
        final_result = re.search(r'(\d+)%', result.stdout)
        percentage = int(float(final_result.group()))

    return f"{percentage}%"

def get_position():
    # Getting the info from playerctl
    result = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "{{ position }}"
        )
    ], capture_output = True, text = True)

    return int(result.stdout.strip())

def get_duration():
    # Getting the info from playerctl
    result = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "{{ mpris:length }}"
        )
    ], capture_output = True, text = True)

    return int(result.stdout.strip())

def get_url():
    # Getting the info from playerctl
    result = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "{{ trunc(xesam:url, 39) }}"
        )
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_status():
    # Getting the rest of the info
    result = subprocess.run([
        "playerctl",
        "status"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_loop():
    # Getting the rest of the info
    result = subprocess.run([
        "playerctl",
        "loop"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_shuffle():
    # Getting the rest of the info
    result = subprocess.run([
        "playerctl",
        "shuffle"
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_user():
    username = getpass.getuser()
    return username

