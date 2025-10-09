import subprocess, getpass, urllib.parse, urllib.request, tempfile
import ascii_magic as magic

# Art to ASCII
def ascii_convert(art_uri):
    # Check file type
    if art_uri is None:
        print("Null file")
        # Display default (like music note)

    # We need to check each URI type
    elif art_uri.startswith("file://"):
        try:
            # Strip "file://" prefix
            new_uri = art_uri[7:]
            # Decode to get rid of possible "%20%20..."
            ascii_art = magic.from_image(urllib.parse.unquote(new_uri))
        # Catch the error
        except OSError as e:
            print(f'Could not load the image', e)

    # Check for URLs
    elif art_uri.startswith("https://"):
        try:
            # Creates a temporary file to store image in
            temp = tempfile.NamedTemporaryFile()
            temp.close()
            # Get the image from the url
            urllib.request.urlretrieve(art_uri, temp.name)
            ascii_art = magic.from_image(temp.name)
        # Catch the error
        except Exception as e :
            print(str(e))

    # Edge cases
    else:
        print("Null file (edge case")

    # Print the actual ascii art
    ascii_art.to_terminal()

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
    # ascii_convert("file:///home/fwtwoo/.mozilla/firefox/firefox-mpris/1385_41.png")
    # ascii_convert("file:///tmp/strawberry-cover-fcoi3x.jpg")
    ascii_convert("https://i.scdn.co/image/ab67616d0000b27315350aa1c89e23a5fa6c0de1")

# Run the program
if __name__ == "__main__":
    main()

# TODO: Add terminal colors at the end like fastfetch or onefetch

