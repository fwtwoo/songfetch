import ascii_magic as magic, urllib.parse, urllib.request, tempfile

# Art to ASCII
def convert(art_uri):
    # Init
    ascii_art = None
    # Check file type
    if art_uri is None or art_uri.strip() == "": # If return empty string
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
    elif art_uri.startswith("https://") or art_uri.startswith("http://"):
        try:
            # Creates a temporary file to store image in
            temp = tempfile.NamedTemporaryFile(delete=False)
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
    if ascii_art:
        ascii_art.to_terminal(columns = 60, width_ratio = 2.2) # Increase columns to make bigger
                                                               # Ratio  2.2 keeps image scaled properly.

