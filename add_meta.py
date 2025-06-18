from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, COMM

# Path to your MP3 file
mp3_file = "samples/file_example_MP3_700KB.mp3"  # ← replace with your actual filename

# Apply standard ID3 metadata
audio = EasyID3(mp3_file)
audio["title"] = "Apshansh"
audio["artist"] = "Artist Example"
audio["album"] = "Example Album"
audio["genre"] = "Indie Folk"
audio["date"] = "2024"
audio["tracknumber"] = "7"
audio["composer"] = "Composer Name"
audio["albumartist"] = "Various Artists"
audio["encodedby"] = "Developer Debarun"
audio["discnumber"] = "1"
audio.save()

# Add extended comment field
id3 = ID3(mp3_file)
id3.add(COMM(encoding=3, desc="desc", text="Extended metadata testing with additional fields."))
id3.save()

print("Metadata successfully added!")
