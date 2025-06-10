# HOW TO USE

1. Activate the Virtual env by - source bin/activate inside the project directory
2. run `pip install -r requirement.txt` - this will install all the libraries
3. then run `python3 main.py <audio file path>`
wait for the result to show up in the terminals and in the output file

4. Ensure ffmpeg is installed (required by librosa & whisper)
If not already installed, 

macOS: brew install ffmpeg

Ubuntu/Debian: sudo apt install ffmpeg

Windows: Download from https://ffmpeg.org/download.html, and add it to your system PATH.
