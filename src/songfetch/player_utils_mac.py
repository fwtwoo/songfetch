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


def run_applescript(script):
    """Helper to run AppleScript and return output"""
    try:
        result = subprocess.run([
            "osascript", "-e", script
        ], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""


def get_backend():
    return "CoreAudio"


def get_player_name():
    try:
        # Check if Music app is running
        script = '''
        tell application "System Events"
            if exists (processes where name is "Music") then
                return "Music"
            else
                return ""
            end if
        end tell
        '''
        if run_applescript(script):
            return "Music"
        return DEFAULTS["player_name"]
    except Exception:
        return DEFAULTS["player_name"]


def get_art():
    # Mac album art is harder to get via AppleScript, return default
    return DEFAULTS["art"]


def get_title():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                return name of current track
            else
                return ""
            end if
        end tell
        '''
        title = run_applescript(script)
        return title if title else DEFAULTS["title"]
    except Exception:
        return DEFAULTS["title"]


def get_artist():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                return artist of current track
            else
                return ""
            end if
        end tell
        '''
        artist = run_applescript(script)
        return artist if artist else DEFAULTS["artist"]
    except Exception:
        return DEFAULTS["artist"]


def get_album():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                return album of current track
            else
                return ""
            end if
        end tell
        '''
        album = run_applescript(script)
        return album if album else DEFAULTS["album"]
    except Exception:
        return DEFAULTS["album"]


def get_duration_formatted():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                set dur to duration of current track
                set mins to dur div 60
                set secs to dur mod 60
                return (mins as string) & ":" & (secs as string)
            else
                return "00:00"
            end if
        end tell
        '''
        duration = run_applescript(script)
        return duration if duration else DEFAULTS["duration_formatted"]
    except Exception:
        return DEFAULTS["duration_formatted"]


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
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                return player position
            else
                return 0
            end if
        end tell
        '''
        pos = run_applescript(script)
        try:
            return int(float(pos))
        except ValueError:
            return DEFAULTS["position"]
    except Exception:
        return DEFAULTS["position"]


def get_duration():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                return duration of current track
            else
                return 0
            end if
        end tell
        '''
        dur = run_applescript(script)
        try:
            return int(float(dur))
        except ValueError:
            return DEFAULTS["duration"]
    except Exception:
        return DEFAULTS["duration"]


def get_url():
    # Mac doesn't typically have URLs for local tracks
    return DEFAULTS["url"]


def get_status():
    try:
        script = '''
        tell application "Music"
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
    except Exception:
        return DEFAULTS["status"]


def get_loop():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                if repeat is on then
                    return "On"
                else
                    return "Off"
                end if
            else
                return "Unknown"
            end if
        end tell
        '''
        loop = run_applescript(script)
        return loop if loop else DEFAULTS["loop"]
    except Exception:
        return DEFAULTS["loop"]


def get_shuffle():
    try:
        script = '''
        tell application "Music"
            if player state is playing or player state is paused then
                if shuffle is on then
                    return "On"
                else
                    return "Off"
                end if
            else
                return "Unknown"
            end if
        end tell
        '''
        shuffle = run_applescript(script)
        return shuffle if shuffle else DEFAULTS["shuffle"]
    except Exception:
        return DEFAULTS["shuffle"]


def get_user():
    try:
        username = getpass.getuser()
        return username if username else DEFAULTS["user"]
    except Exception:
        return DEFAULTS["user"]
