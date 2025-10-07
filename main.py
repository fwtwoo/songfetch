import subprocess
import getpass

# Main function
def main():
    p = "hi"
    # Get the current player seperately
    player = subprocess.run([
        "playerctl", "metadata", "--format", "{{ playerName }}"
    ], capture_output = True, text = True)

    # Getting the track info from playerctl
    track_data = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "Title: {{ title }}\n"
            "Artist: {{ artist }}\n"
            "Album: {{ album }}\n"
            "Duration: {{ duration(mpris:length) }}"
        )
    ], capture_output = True, text = True)

    # Getting the player info from playerctl
    player_data = subprocess.run([
        "playerctl",
        "metadata",
        "--format", (
            "Position: {{ duration(position) }}\n"
            "URL: {{ trunc(xesam:url, 39) }}"
        )
    ], capture_output = True, text = True)

    # Getting the rest of the info
    status_data = subprocess.run([
        "playerctl",
        "status"
    ], capture_output = True, text = True)

    # Define some variables for later
    username = getpass.getuser()

    # Define some strings we'll need to print
    line = "─────────────────────────────────────────────"
    now_playing = "🎵 Now Playing"
    player_info = "🎧 Player Info"

    # Print username and track data
    print("{0}@{1}".format(username, player.stdout.strip()))
    print(f"{line}\n{now_playing}\n{line}")
    print(track_data.stdout.strip())

    # Print player data
    print(f"{line}\n{player_info}\n{line}")
    print(player_data.stdout.strip())
    print(f"Status: {status_data.stdout.strip()}")

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

