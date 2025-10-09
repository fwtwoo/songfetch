import subprocess, getpass

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

def get_track():
    # Getting various track info from playerctl
    result = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "Title: {{ title }}\n"
            "Artist: {{ artist }}\n"
            "Album: {{ album }}\n"
            "Duration: {{ duration(mpris:length) }}"
        )
    ], capture_output = True, text = True)

    return result.stdout.strip()

def get_player():
    # Getting the player info from playerctl
    result = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "Position: {{ duration(position) }}\n"
            "URL: {{ trunc(xesam:url, 39) }}"
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

# Use get_backend() to get current volume
def get_volume():
    current_backend = get_backend()
    if current_backend is "PipeWire":
        # do
    elif current_backend is "PulseAudio":
        # do
    else:
        # do

def get_user():
    username = getpass.getuser()
    return username

