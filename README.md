# Audio Metadata Analyzer & Enricher with AI

This project is a cross-platform, AI-powered audio metadata analysis and enrichment tool. It extracts and enhances metadata from audio files, including title, artist, genre, language, transcription, and mood detection. The system also ensures file integrity using virus scanning and provides multilingual support.

## 📄 Project Overview

The project is designed to:

* Extract technical metadata (duration, bitrate, sample rate, etc.)
* Detect and embed descriptive metadata (artist, album, genre, track, etc.)
* Transcribe spoken audio
* Detect the language of speech in the file
* Estimate mood/genre using machine learning models
* Provide API-based or script-based access (usable from Laravel, Python CLI, etc.)

This can serve as a full-fledged **AI/ML Capstone Study Project** for:

* Audio signal processing
* Machine learning in audio understanding
* Full-stack Python + Web (Laravel) integration

---

## 🌐 Supported Platforms & Installation

### Python (Required)

* Python 3.8+
* Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate.bat     # Windows
```

### Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

**OR manually:**

```bash
pip install mutagen openai-whisper langdetect pycountry requests rich
```

For FFmpeg (used by Whisper and audio probing):

#### MacOS:

```bash
brew install ffmpeg
```

#### Windows:

1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Add FFmpeg to PATH

#### Linux:

```bash
sudo apt install ffmpeg
```

---

## 🧠 AI / ML Models Used

| Feature            | Model / Tool                                     | Description                                       |
| ------------------ | ------------------------------------------------ | ------------------------------------------------- |
| Transcription      | OpenAI Whisper                                   | Converts speech to text                           |
| Language Detection | `langdetect`                                     | Predicts language from transcribed text           |
| Mood Detection     | Scikit-learn or AudioSet pretrained classifier   | Classifies emotion/genre based on audio signature |
| Metadata Handling  | Mutagen (ID3)                                    | Reads/Writes metadata in MP3 files                |
| Malware Check      | Optional via open-source VirusTotal alternatives |                                                   |

---

## 📊 Project Structure

```bash
project/
├── extractor.py        # Main metadata + AI enrichment script
├── utils/
│   ├── mood_model.py   # Mood/genre classification
│   └── language_utils.py
├── audio/
│   └── input_files     # Upload audio files here
├── output/
│   └── enriched_files  # Processed output files
├── api/
│   └── laravel_integration.md # API notes for Laravel
├── requirements.txt
└── README.md
```

---

## 🎓 Academic Relevance

This project can be submitted as a **capstone or thesis project** in the following fields:

* Artificial Intelligence / Machine Learning
* Natural Language Processing
* Digital Signal Processing
* Audio Engineering
* Software Engineering (Full Stack)

**Unique Qualifiers:**

* Real-world applicability (transcription, tagging, malware scanning)
* Integrates AI (Whisper, mood classification)
* Usable in production (via Laravel or Python CLI)

---

## 📈 Future Enhancements

* Speaker recognition
* Genre clustering with deep learning (VGGish)
* Web frontend with preview and tagging interface
* Batch processing via drag-and-drop

---

## 🚜 Get Started

1. Activate the Virtual env by - source bin/activate inside the project directory
2. run `pip install -r requirement.txt` - this will install all the libraries
3. then run `python3 main.py <audio file path>`
wait for the result to show up in the terminals and in the output file

4. **Ensure ffmpeg is installed** (required by *librosa & whisper*)
If not already installed, 

**macOS**: `brew install ffmpeg`

**Ubuntu/Debian**: `sudo apt install ffmpeg`

**Windows**: Download from <ins>https://ffmpeg.org/download.html</ins>, and add it to your system PATH.

**NB :** There is an issue with the installation openai-whisper package in python 3.13 version. so we are installing it directly from git. 
you can see the requirement txt file to know more.

**How to run it**
------------------
1. go to the project directory
2. if you are in linux or mac activate the virtual environment by `source bin/activate` 
    if windows use `bin/activate`
3. then run python main.py `<file name>`
4. to deactivate the virtual environment  `deactivate`   


**NB : Please note, This is a still ongoing project.**