from ascii_convert import convert
from player_utils import (
    get_art,
    get_loop,
    get_shuffle,
    get_player_name,
    get_status,
    get_track,
    get_user,
    get_volume,
    get_url,
    get_backend,
    get_duration,
    get_position
)

def progress_bar():
    # Calculate percentage
    pos = get_position()
    dur = get_duration()
    percentage = pos / dur

    # Calculate filled and empty characters
    filled = int(percentage * 16)
    empty = 16 - filled
    fprint = "▓" * filled
    eprint = "░" * empty

    # Calculate position and duration seperately
    pos_seconds = int(pos / 1000000)
    dur_seconds = int(dur / 1000000)

    # Nicer representation
    display_pos = f"{pos_seconds // 60:02d}:{pos_seconds % 60:02d}"
    display_dur = f"{dur_seconds // 60:02d}:{dur_seconds % 60:02d}"

    # Full representation
    display_str = f" {display_pos} / {display_dur} ({round(percentage * 100)}%)"

    return fprint + eprint + display_str

# Main function
def main():
    # Define some strings we'll need to print
    line = "─────────────────────────────────────────────"
    now_playing = "🎵 Now Playing"
    playback_info = "🎧 Playback Info"
    audio_system = "🎧 Audio System"

    # Print username and track data
    print("{0}@{1}".format(get_user(), get_player_name()))
    print(f"{line}\n{now_playing}\n{line}")
    print(get_track())
    print(progress_bar())

    # Print player data
    print(f"{line}\n{playback_info}\n{line}")
    print(f"Status: {get_status()}")
    print(f"Volume: {get_volume()}")
    print(f"Loop: {get_loop()}")
    print(f"Shuffle: {get_shuffle()}")
    print(f"Player: {get_player_name()}")
    print(get_url())

    # Print system data
    print(f"{line}\n{audio_system}\n{line}")
    print(f"Backend: {get_backend()}")

    # Print ASCII album art
    new = convert(get_art())
    for line in new:
        print(line)

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

