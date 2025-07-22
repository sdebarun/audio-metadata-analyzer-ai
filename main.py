import os
import json
from mutagen import File as MutagenFile
from mutagen.id3 import ID3, APIC
import subprocess
import numpy as np
import librosa
import hashlib
import requests
import pycountry
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where() #~ for certificate issue. Should work cross-platform on OS

# lyrics and language detection (if paid scheme then optional)
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Optional: Add your VirusTotal API key here #todo - need opensource alternatives
VT_API_KEY = os.getenv("VT_API_KEY", "")

#converting iso code to full name language  (for whisper laguage output)
def get_language_name(iso639_1_code):
    try:
        language = pycountry.languages.get(alpha_2=iso639_1_code)
        return language.name
    except AttributeError:
        return "Language name not found"


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
    model = whisper.load_model("tiny")
    result = model.transcribe(file_path)
    return {
        "text": result.get("text"), #! ASCII ISSUE - need to resolve (ensure_ascii = false throws error of undefined unicode)
        "language": result.get("language")  # ISO 639-1 language code (e.g., 'hi' for Hindi)
    }


def detect_genre_mood(file_path):
    try:
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)

        mood = "energetic" if tempo > 120 else "calm"
        genre = "electronic" if np.mean(zcr) > 0.1 else "acoustic"

        return {
            "tempo": tempo,
            "mood": mood,
            "genre_estimate": genre,
            # "chromagrams" : chroma,
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
    response = requests.get(url, headers=headers, verify=False)

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
        metadata['language_detected'] =get_language_name(transcribe_audio(file_path).get("language"))
    else:
        metadata["transcription"] = "Whisper not available. Install with: pip install openai-whisper"

    return metadata

# numpy nd array cleaner mostly
def clean_for_json(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_for_json(i) for i in obj]
    return obj

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(json.dumps('No Argument supplied. Exiting...', indent=4))
        sys.exit(1)

    audio_file = sys.argv[1]
    # print(audio_file)
    if not os.path.exists(audio_file):
        print("File does not exist.")
        sys.exit(1)

    metadata = extract_all_metadata(audio_file)
    print(json.dumps(clean_for_json(metadata), indent=4))


    # the json file where the output must be stored

    out_file = open("output.json", "w")

    print(json.dump(clean_for_json(metadata), out_file, indent = 6))

    out_file.close()    

