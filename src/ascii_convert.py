import ascii_magic as magic, urllib.parse, urllib.request, tempfile

def default_art(file="default_art.txt"):
    # Get the default music note art from file
    with open(file, "r", encoding="utf-8") as f:
        return f.read().split('\n')

# Art to ASCII
def convert(art_uri):
    # Init variables
    ascii_art_lines = None
    # Check file type
    if art_uri is None or art_uri.strip() == "": # If return empty string
        return default_art()

    # We need to check each URI type
    elif art_uri.startswith("file://"):
        try:
            # Strip "file://" prefix
            new_uri = art_uri[7:]
            # Decode to get rid of possible "%20%20..."
            ascii_art = magic.from_image(urllib.parse.unquote(new_uri))
            # Convert to ascii
            ascii_string = ascii_art.to_ascii(columns = 60, width_ratio = 2.2)
            aascii_art_lines = ascii_string.split('\n')

        # Catch the error
        except OSError as e:
            return default_art()

    # Check for URLs
    elif art_uri.startswith("https://") or art_uri.startswith("http://"):
        try:
            # Creates a temporary file to store image in
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.close()
            # Get the image from the url
            urllib.request.urlretrieve(art_uri, temp.name)
            ascii_art = magic.from_image(temp.name)
            # Convert to ascii
            ascii_string = ascii_art.to_ascii(columns = 60, width_ratio = 2.2)
            aascii_art_lines = ascii_string.split('\n')

        # Catch the error
        except Exception as e :
            return default_art()

    # Edge cases
    else:
        return default_art()

    # Print the actual ascii art
    if ascii_art_lines:
        return ascii_art_lines
    else:
        return default_art()

