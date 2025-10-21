import subprocess
import getpass

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

# Supported players and their AppleScript apps
SUPPORTED_PLAYERS = {
    "Spotify": "Spotify",
    "Music": "Music",
    "iTunes": "iTunes",  # For older macOS
}

_current_player = None


def run_applescript(script):
    """Helper to run AppleScript and return output"""
    try:
        result = subprocess.run([
            "osascript", "-e", script
        ], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""


def detect_current_player():
    """Detect which media player is currently active/playing"""
    global _current_player

    for player_name, app_name in SUPPORTED_PLAYERS.items():
        script = f'''
        tell application "System Events"
            if exists (processes where name is "{app_name}") then
                tell application "{app_name}"
                    if player state is playing or player state is paused then
                        return "{player_name}"
                    end if
                end tell
            end if
        end tell
        return ""
        '''
        result = run_applescript(script)
        if result:
            _current_player = result
            return result

    _current_player = None
    return None


def get_current_player():
    """Get the current player, detecting if not set"""
    if _current_player is None:
        detect_current_player()
    return _current_player


def get_player_name():
    player = get_current_player()
    if player:
        return player
    return DEFAULTS["player_name"]


def get_art():
    # Album art is not easily accessible via AppleScript for most players
    return DEFAULTS["art"]


def get_title():
    player = get_current_player()
    if not player:
        return DEFAULTS["title"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                return name of current track
            end if
        end tell
        '''
    else:  # Music or iTunes
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                return name of current track
            end if
        end tell
        '''

    title = run_applescript(script)
    return title if title else DEFAULTS["title"]


def get_artist():
    player = get_current_player()
    if not player:
        return DEFAULTS["artist"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                return artist of current track
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                return artist of current track
            end if
        end tell
        '''

    artist = run_applescript(script)
    return artist if artist else DEFAULTS["artist"]


def get_album():
    player = get_current_player()
    if not player:
        return DEFAULTS["album"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                return album of current track
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                return album of current track
            end if
        end tell
        '''

    album = run_applescript(script)
    return album if album else DEFAULTS["album"]


def get_duration_formatted():
    player = get_current_player()
    if not player:
        return DEFAULTS["duration_formatted"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                set dur to duration of current track
                set mins to dur div 60
                set secs to dur mod 60
                return (mins as string) & ":" & text -2 thru -1 of ("0" & secs)
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                set dur to duration of current track
                set mins to dur div 60
                set secs to dur mod 60
                return (mins as string) & ":" & text -2 thru -1 of ("0" & secs)
            end if
        end tell
        '''

    duration = run_applescript(script)
    return duration if duration else DEFAULTS["duration_formatted"]


def get_volume():
    try:
        script = '''
        set vol to output volume of (get volume settings)
        return vol as string
        '''
        vol = run_applescript(script)
        if vol.isdigit():
            return f"{vol}%"
        return DEFAULTS["volume"]
    except Exception:
        return DEFAULTS["volume"]


def get_position():
    player = get_current_player()
    if not player:
        return DEFAULTS["position"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    script = f'''
    tell application "{app_name}"
        if player state is playing or player state is paused then
            return player position
        end if
    end tell
    '''

    pos = run_applescript(script)
    try:
        return int(float(pos))
    except ValueError:
        return DEFAULTS["position"]


def get_duration():
    player = get_current_player()
    if not player:
        return DEFAULTS["duration"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                return duration of current track
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                return duration of current track
            end if
        end tell
        '''

    dur = run_applescript(script)
    try:
        return int(float(dur))
    except ValueError:
        return DEFAULTS["duration"]


def get_url():
    # URLs are not typically available for local tracks
    return DEFAULTS["url"]


def get_status():
    player = get_current_player()
    if not player:
        return DEFAULTS["status"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    script = f'''
    tell application "{app_name}"
        set state to player state
        if state is playing then
            return "Playing"
        else if state is paused then
            return "Paused"
        else
            return "Stopped"
        end if
    end tell
    '''

    status = run_applescript(script)
    return status if status else DEFAULTS["status"]


def get_loop():
    player = get_current_player()
    if not player:
        return DEFAULTS["loop"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        # Spotify doesn't have loop in AppleScript, return Unknown
        return DEFAULTS["loop"]
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                if repeat is on then
                    return "On"
                else
                    return "Off"
                end if
            end if
        end tell
        '''

    loop = run_applescript(script)
    return loop if loop else DEFAULTS["loop"]


def get_shuffle():
    player = get_current_player()
    if not player:
        return DEFAULTS["shuffle"]

    app_name = SUPPORTED_PLAYERS.get(player, "Music")

    if player == "Spotify":
        # Spotify shuffle status via AppleScript
        script = '''
        tell application "Spotify"
            if player state is playing or player state is paused then
                if shuffling is true then
                    return "On"
                else
                    return "Off"
                end if
            end if
        end tell
        '''
    else:
        script = f'''
        tell application "{app_name}"
            if player state is playing or player state is paused then
                if shuffle is on then
                    return "On"
                else
                    return "Off"
                end if
            end if
        end tell
        '''

    shuffle = run_applescript(script)
    return shuffle if shuffle else DEFAULTS["shuffle"]


def get_user():
    try:
        username = getpass.getuser()
        return username if username else DEFAULTS["user"]
    except Exception:
        return DEFAULTS["user"]


# Backend is CoreAudio
def get_backend():
    return "CoreAudio"
