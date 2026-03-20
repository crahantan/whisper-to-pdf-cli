import argparse
import os
import sys
from datetime import timedelta
from pathlib import Path

import whisper
from fpdf import FPDF


class TranscriptionPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 12)
        self.cell(
            0,
            10,
            "Transcription",
            border=0,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def create_pdf(segments, output_path):
    pdf = TranscriptionPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)

    for segment in segments:
        start = str(timedelta(seconds=int(segment["start"])))
        end = str(timedelta(seconds=int(segment["end"])))
        timestamp = f"[{start} --> {end}]"
        text = segment["text"].strip()

        pdf.set_text_color(100, 100, 100)
        pdf.write(5, f"{timestamp} ")
        pdf.set_text_color(0, 0, 0)
        pdf.write(5, f"{text}\n\n")

    pdf.output(str(output_path))


def main():

    parser = argparse.ArgumentParser(
        description="Whisper to PDF CLI Tool",
        epilog="Example: python main.py -m large -l es interview.mp3 -o ./outputs",
    )

    parser.add_argument(
        "-m",
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper AI model size. Larger models are more accurate but slower (default: 'base')",
    )

    parser.add_argument(
        "-l",
        "--language",
        default="es",
        help="Language code for transcription (e.g., 'en', 'es', 'fr'). Default: 'es'",
    )

    parser.add_argument(
        "input", help="Path to the input audio file (e.g., audio.mp3, recording.wav)"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="outputs",
        help="Directory where the PDF will be saved (default: 'outputs')",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error:The file '{args.input}' does not exist")
        return

    audio_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_output = output_dir / f"{audio_path.stem}.pdf"

    print(f"[*] Loading model '{args.model}'...")

    try:
        model = whisper.load_model(args.model)
    except Exception as e:
        print(f"[!] Critical Error: {e}")
        return

    print(f"[*] Transcribing... (this might take a moment)")
    result = model.transcribe(str(audio_path), language=args.language)

    print(f"[*] Exporting to PDF...")
    create_pdf(result["segments"], pdf_output)

    print(f"\n[+] Success! File saved at: {pdf_output}")


if __name__ == "__main__":
    main()
