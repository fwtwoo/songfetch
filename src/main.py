from ascii_convert import convert
from player_utils import (
    get_art,
    get_loop,
    get_shuffle,
    get_player_name,
    get_status,
    get_title,
    get_artist,
    get_album,
    get_duration_formatted,
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

def get_info_line():
    # Get some strings to use later
    line = "─────────────────────────────────────────────"
    now_playing = "🎵 Now Playing"
    playback_info = "🎧 Playback Info"
    audio_system = "🔊 Audio System"

    # Here we concatenate all the info into one list
    info_lines = [
        # Print username and track data
        f"{get_user()}@{get_player_name()}",
        line, now_playing, line,
        f"Title: {get_title()}",
        f"Artist: {get_artist()}",
        f"Album: {get_album()}",
        f"Duration: {get_duration_formatted()}",
        f"{progress_bar()}",

        # Print player data
        line, playback_info, line,
        f"Status: {get_status()}",
        f"Volume: {get_volume()}",
        f"Loop: {get_loop()}",
        f"Shuffle: {get_shuffle()}",
        f"Player: {get_player_name()}",
        f"URL: {get_url()}",

        # Print system data
        line, audio_system, line,
        f"Backend: {get_backend()}"
    ]

    return info_lines

# Main function
def main():
    # Define the two lists to iterate over
    print()
    art_col = convert(get_art())
    info_col = get_info_line()

    # Code found on stackoverflow (saved me hella time lol) to print
    # lists next to each other when one list may be longer than the other:

    # Find the longest line in both column lists
    max_art = max(len(x) for x in art_col)
    max_info = max(len(y) for y in info_col)
 
    # Compare lenghts
    if len(art_col) > len(info_col):
        # Replace but with added padding (spaces)
        new_info_col = info_col + [''] * (len(art_col) - len(info_col))
        # Loop through all lines in art
        for i in range(len(art_col)):
            print(f"{art_col[i]:{max_art}}{new_info_col[i]:{max_info}}")

    else:
        # Pad but the othre way around
        new_art_col = art_col + [''] * (len(info_col) - len(art_col))
        # Loop all lines in info
        for j in range(len(info_col)):
            print(f"{new_art_col[j]:{max_art}}{info_col[j]:{max_info}}")

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

