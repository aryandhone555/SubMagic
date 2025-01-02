# SubMagic
This is a Python-based desktop application that allows users to add subtitles to videos using audio transcription. The application uses OpenAI's Whisper model for audio transcription and MoviePy for adding subtitles to videos.

## Features
- Extracts audio from a video file.
- Transcribes audio to text using Whisper.
- Adds subtitles to videos with customizable font colors.
- Outputs the final subtitled video in MP4 format.

## Prerequisites
1. Install Python 3.7 or higher.
2. Install FFmpeg (required for `moviepy` and `ffmpeg-python`):
   - Download FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html).
   - Add FFmpeg to your system's PATH.

3. Install ImageMagick (required for `moviepy`'s `TextClip`):
   - Download ImageMagick from [ImageMagick.org](https://imagemagick.org/script/download.php).
   - Add ImageMagick to your system's PATH.
   - Ensure the `convert` command is available by verifying the ImageMagick installation.

4. Install the required Python packages listed in `requirements.txt`.

## Installation
1. Clone or download this repository.
2. Open a terminal and navigate to the directory containing this project.
3. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
