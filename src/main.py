from ascii_convert import convert
from player_utils import (get_art,
    get_loop,
    get_shuffle,
    get_player_name,
    get_status,
    get_track,
    get_user,
    get_volume,
    get_url,
    get_backend
)

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
    # ADD progress bar

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
    convert(get_art())

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

