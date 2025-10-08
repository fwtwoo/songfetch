import subprocess, getpass
import ascii_magic as magic

# Art to ASCII
def ascii_convert(art_uri):
    # Check file type
    if "file://" in art_uri:
        # Strip "file://" prefix
        print("Local file")
        file_uri = art_uri.replace("file://", "")
        return file_uri
        # Maybe add extension if not exists?
    elif "https://" or "http://" in art_uri:
        print("Remote link")
        # Download image
        # Display it
    elif art_uri is None:
        print("Null file")
        # Display default (like music note)
    else:
        print("Null file (else)")
        # Display default
    try:
        ascii_art = magic.from_url(art_uri)
        ascii_art = magic.from_image(art_uri)
        ascii_art.to_terminal()
    except OSError as e:
        print(f'Could not load the image', e)

# Main function
def main():
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

    # Test ASCII convert and print
    #ascii_convert('https://i.scdn.co/image/ab67616d0000b273c1a13209dfe146aef3296e34')
    ascii_convert("file:///home/fwtwoo/.mozilla/firefox/firefox-mpris/1385_36.png")

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

