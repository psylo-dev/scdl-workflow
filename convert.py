from moviepy.editor import *  # Importiere MoviePy
import sys

def convert_to_video(audio_file, image_file, output_file):
    # Lade die Audiodatei und das Bild
    audio = AudioFileClip(audio_file)
    image = ImageClip(image_file, duration=audio.duration)  # Setze die Dauer des Bildes auf die Dauer der Audiodatei
    image = image.set_fps(24)  # Setze die Bildrate

    # Kombiniere Bild und Audio
    video = image.set_audio(audio)

    # Schreibe das Ergebnis als MP4-Datei
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 convert.py <audio_file> <image_file> <output_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    image_file = sys.argv[2]
    output_file = sys.argv[3]

    convert_to_video(audio_file, image_file, output_file)
