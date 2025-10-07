import subprocess
import getpass

username = getpass.getuser()
line = "─────────────────────────────────────────────"
now_playing = "🎵 Now Playing"
player_info = "🎧 Player Info"

player = subprocess.run(["playerctl", "metadata", "--format", "{{ playerName }}"], capture_output=True, text=True)
title = subprocess.run(["playerctl", "metadata", "title"], capture_output=True, text=True)
artist = subprocess.run(["playerctl", "metadata", "artist"], capture_output=True, text=True)
album = subprocess.run(["playerctl", "metadata", "album"], capture_output=True, text=True)
duration = subprocess.run(["playerctl", "metadata", "--format", "{{ duration(mpris:length) }}"], capture_output=True, text=True)

position = subprocess.run(["playerctl", "metadata", "--format", "{{ duration(position) }}"], capture_output=True, text=True)
status = subprocess.run(["playerctl", "status"], capture_output=True, text=True)
url = subprocess.run(["playerctl", "metadata", "--format", "{{ trunc(xesam:url, 45) }}"], capture_output=True, text=True)

print("{0}@{1}".format(username, player.stdout.strip()))
print(line)
print(now_playing)
print(line)

print(title.stdout.strip())
print(artist.stdout.strip())
print(album.stdout.strip())
print(duration.stdout.strip())

print(line)
print(player_info)
print(line)

print(position.stdout.strip())
print(status.stdout.strip())
print(url.stdout.strip())

