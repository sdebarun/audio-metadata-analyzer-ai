import os
import json
from mutagen import File as MutagenFile
from mutagen.id3 import ID3, APIC
import subprocess
import numpy as np
import librosa
import hashlib
import requests

# Optional: Use whisper for transcript if installed
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Optional: Add your VirusTotal API key here
VT_API_KEY = os.getenv("VT_API_KEY", "d914951e55d48368cb89361495b988b26868c215302117d2ec2344529214c935")


def extract_basic_metadata(file_path):
    audio = MutagenFile(file_path, easy=True)
    metadata = {
        "tags": dict(audio.tags) if audio.tags else {},
        "info": str(audio.info) if audio else "N/A"
    }
    return metadata


def extract_cover_art(file_path):
    try:
        audio = ID3(file_path)
        for tag in audio.values():
            if isinstance(tag, APIC):
                cover_path = file_path + "_cover.jpg"
                with open(cover_path, "wb") as img:
                    img.write(tag.data)
                return cover_path
    except Exception:
        pass
    return None


def extract_technical_details(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "format=duration:stream=bit_rate,sample_rate,channels",
           "-of", "json", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout)


def transcribe_audio(file_path):
    if not WHISPER_AVAILABLE:
        return "Whisper not installed"
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result.get("text")


def detect_genre_mood(file_path):
    try:
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)

        mood = "energetic" if tempo > 120 else "calm"
        genre = "electronic" if np.mean(zcr) > 0.1 else "acoustic"

        return {
            "tempo": tempo,
            "mood": mood,
            "genre_estimate": genre,
            "spectral_centroid_mean": np.mean(spectral_centroid).item(),
            "zero_crossing_rate_mean": np.mean(zcr).item()
        }
    except Exception as e:
        return {"error": str(e)}


def check_malware(file_path):
    if not VT_API_KEY:
        return {"status": "VirusTotal API key not set."}

    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    headers = {"x-apikey": VT_API_KEY}
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return {"malware_analysis": stats}
    elif response.status_code == 404:
        return {"status": "File not found in VirusTotal database."}
    else:
        return {"status": f"Error querying VirusTotal: {response.status_code}"}


def extract_all_metadata(file_path):
    metadata = {
        "basic": extract_basic_metadata(file_path),
        "technical": extract_technical_details(file_path),
        "cover_art_path": extract_cover_art(file_path),
        "genre_mood_analysis": detect_genre_mood(file_path),
        "malware_scan": check_malware(file_path)
    }

    if WHISPER_AVAILABLE:
        metadata["transcription"] = transcribe_audio(file_path)
    else:
        metadata["transcription"] = "Whisper not available. Install with: pip install openai-whisper"

    return metadata


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_metadata.py <audiofile>")
        sys.exit(1)

    audio_file = sys.argv[1]
    print(audio_file)
    if not os.path.exists(audio_file):
        print("File does not exist.")
        sys.exit(1)

    metadata = extract_all_metadata(audio_file)
    print(json.dumps(metadata, indent=4))
