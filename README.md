# Transcriber

A Python-based audio transcription tool using WhisperX.

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/skssmd/transcriber.git
cd transcriber
```
2. **Create and activate a virtual environment**

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
3. **Install required Python packages**

```bash
pip install -r requirements.txt
Install FFmpeg
```
FFmpeg is required for audio processing.

On Windows, you can install it using winget:

```bash
winget install ffmpeg
```
Make sure ffmpeg is added to your system PATH.
