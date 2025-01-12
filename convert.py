from moviepy.editor import *  # Importiere MoviePy
import sys
import os

def convert_to_video(audio_file, image_file, output_file):
    """
    Diese Funktion konvertiert eine Audiodatei und ein Bild in ein Video,
    wobei das Bild als Standbild für die Dauer des Audios verwendet wird.

    :param audio_file: Der Pfad zur Audiodatei (MP3, WAV, etc.)
    :param image_file: Der Pfad zum Bild, das als Standbild im Video verwendet wird
    :param output_file: Der Pfad, an dem die resultierende MP4-Datei gespeichert wird
    """
    print(f"Starte die Konvertierung: {audio_file}")  # Gebe die Audiodatei aus, die gerade verarbeitet wird

    # Lade die Audiodatei mit MoviePy
    audio = AudioFileClip(audio_file)  # Audio wird geladen und für die Dauer des Videos verwendet
    
    # Lade das Bild und setze die Dauer des Bildes gleich der Dauer der Audiodatei
    image = ImageClip(image_file, duration=audio.duration)  # Bild wird angezeigt, solange das Audio läuft
    
    # Setze die Bildrate auf 24 Frames pro Sekunde (Standard für Videos)
    image = image.set_fps(24)  # Eine gängige Bildrate für Videos

    # Kombiniere das Bild mit dem Audio
    video = image.set_audio(audio)  # Setze das Audio als Tonspur des Videos

    # Schreibe das Video als MP4-Datei mit den angegebenen Codecs
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    print(f"Konvertierung abgeschlossen: {output_file}")  # Gebe die fertige Datei aus

def find_audio_files(download_path):
    """
    Diese Funktion listet alle MP3-Dateien im angegebenen Verzeichnis auf.
    
    :param download_path: Der Pfad, in dem nach MP3-Dateien gesucht wird
    :return: Liste der gefundenen MP3-Dateien
    """
    audio_files = [f for f in os.listdir(download_path) if f.endswith('.mp3')]
    
    if not audio_files:
        print("Keine MP3-Dateien gefunden.")
    else:
        print(f"Gefundene MP3-Dateien: {', '.join(audio_files)}")
    
    return audio_files

if __name__ == "__main__":
    # Überprüfe, ob die richtigen Argumente übergeben wurden
    if len(sys.argv) != 4:
        print("Usage: python3 convert.py <audio_file> <image_file> <output_file>")
        sys.exit(1)  # Beende das Skript, wenn nicht die erwartete Anzahl an Argumenten vorliegt

    # Die Argumente werden von der Kommandozeile übergeben
    audio_file = sys.argv[1]  # Erster Parameter: Der Pfad zur Audiodatei
    image_file = sys.argv[2]  # Zweiter Parameter: Der Pfad zum Bild
    output_file = sys.argv[3]  # Dritter Parameter: Der Pfad zur Ausgabedatei (Video)

    # Überprüfe, ob die angegebenen Dateien existieren
    if not os.path.isfile(audio_file):
        print(f"Fehler: Audiodatei {audio_file} wurde nicht gefunden.")
        sys.exit(1)

    if not os.path.isfile(image_file):
        print(f"Fehler: Bilddatei {image_file} wurde nicht gefunden.")
        sys.exit(1)

    # Rufe die Funktion zur Konvertierung von Audio und Bild zu Video auf
    convert_to_video(audio_file, image_file, output_file)
