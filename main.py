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
            "Transcripción de Audio",
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
    if len(sys.argv) < 2:
        print("Use: python main.py <audio_file> [output_directory]")
        sys.exit(1)

    audio_path = sys.argv[1]
    target_folder = sys.argv[2] if len(sys.argv) > 2 else "outputs"

    if not os.path.exists(audio_path):
        print(f"Error: The file '{audio_path}' doesn't exist")
        sys.exit(1)

    output_dir = Path(target_folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(target_folder)
    pdf_output = output_dir / f"{file_name}.pdf"

    print(f"Loading Whisper Model...")
    model = whisper.load_model("base")

    print(f"Processing: {audio_path}")
    print(f"Destiny: {output_dir}/")

    result = model.transcribe(audio_path, language="es")

    create_pdf(result["segments"], pdf_output)
    print(f"Ready!, PDF on: {pdf_output}")


if __name__ == "__main__":
    main()
