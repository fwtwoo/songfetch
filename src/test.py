import ascii_magic as magic

ascii_art = magic.from_image("default.jpg")
ascii_string = ascii_art.to_ascii(columns = 60, width_ratio = 2.2)

with open("default_art.txt", "w") as f:
    f.write(ascii_string)
