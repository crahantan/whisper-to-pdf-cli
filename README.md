# Whisper Audio to PDF (CLI Tool)

A lightweight Python utility to transcribe audio files locally using the **OpenAI Whisper** model. It generates a clean PDF report with precise timestamps, perfect for lectures, interviews, or meetings.

---

## System Requirements (Arch Linux)

This tool requires **FFmpeg** for audio processing. Install it along with Python's package manager:

```bash
sudo pacman -S ffmpeg python-pip
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/crahantan/whisper-to-pdf-cli.git
   cd whisper-to-pdf-cli
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The script accepts the audio file path an optional output directory as the second.

```bash
usage: main.py [-h] [-m {tiny,base,small,medium,large}] [-l LANGUAGE] [-o OUTPUT] input

Whisper to PDF CLI Tool

positional arguments:
  input                 Path to the input audio file (e.g., audio.mp3, recording.wav)

options:
  -h, --help            show this help message and exit
  -m, --model {tiny,base,small,medium,large}
                        Whisper AI model size. Larger models are more accurate but slower (default: 'base')
  -l, --language LANGUAGE
                        Language code for transcription (e.g., 'en', 'es', 'fr'). Default: 'es'
  -o, --output OUTPUT   Directory where the PDF will be saved (default: 'outputs')

Example: python main.py -m large -l es interview.mp3 -o ./outputs
```


## Key Features
- **100% Local Transcription:** Powered by OpenAI Whisper. No data is sent to the cloud, ensuring total privacy.
- **Structured PDF Export:** Generates professional documents with grayed-out timestamps and clear text formatting using `fpdf2`.
- **Smart Directory Handling:** Automatically creates destination folders if they don't exist.
- **High Precision:** Defaulted to Spanish (`language="es"`) but easily adjustable for multi-language support.

## Project Structure
- `main.py`: Core logic for transcription and PDF generation.
- `requirements.txt`: List of dependencies (Whisper, FPDF2, Torch).
- `.gitignore`: Configured for Arch Linux, Python, and virtual environments.

---

## License
MIT License - Feel free to use and modify for your own projects.
