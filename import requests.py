import requests
from collections import Counter

playlist_id = "15483271781"
url = f"https://api.deezer.com/playlist/15483271781/tracks?limit=1000"

data = requests.get(url).json()

tracks = data["data"]

artists = Counter()
for track in tracks:
    artists[track["artist"]["name"]] += 1

print(f"Total tracks: {len(tracks)}")
print("\nTop artists:")

for artist, count in artists.most_common(30):
    print(f"{artist}: {count}")