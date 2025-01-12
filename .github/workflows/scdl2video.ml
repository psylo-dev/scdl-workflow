name: SoundCloud Download & Video Conversion

on:
  workflow_dispatch:
    inputs:
      url:
        description: 'SoundCloud URL (Track/Playlist/User)'
        required: true
        default: 'https://soundcloud.com/psylobrain/sets/psyauto'
      stock_image:
        description: 'Pfad zu einem Stock-Image (z. B. cover.jpg)'
        required: true
        default: 'cover.jpg'

jobs:
  download_and_convert:
    runs-on: ubuntu-latest

    steps:
      # 1. Repository auschecken
      - name: Repository auschecken
        uses: actions/checkout@v3

      # 2. Python einrichten
      - name: Python einrichten
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      # 3. FFmpeg installieren
      - name: FFmpeg installieren
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg

      # 4. SCDL installieren
      - name: SCDL installieren
        run: pip install git+https://github.com/scdl-org/scdl.git

      # 5. Standardpfade festlegen
      - name: Standardpfade festlegen
        id: define_paths
        run: |
          SYNC_FILE="${GITHUB_WORKSPACE}/archive.txt"
          DOWNLOAD_PATH="${GITHUB_WORKSPACE}/downloads"
          VIDEO_OUTPUT_PATH="${GITHUB_WORKSPACE}/videos"
          STOCK_IMAGE="${GITHUB_WORKSPACE}/${{ github.event.inputs.stock_image }}"
          
          # Ordner erstellen
          mkdir -p "$DOWNLOAD_PATH"
          mkdir -p "$VIDEO_OUTPUT_PATH"
          mkdir -p "$(dirname "$SYNC_FILE")"
          [ -f "$SYNC_FILE" ] || touch "$SYNC_FILE"
          
          echo "download_path=$DOWNLOAD_PATH" >> $GITHUB_ENV
          echo "video_output_path=$VIDEO_OUTPUT_PATH" >> $GITHUB_ENV
          echo "stock_image=$STOCK_IMAGE" >> $GITHUB_ENV

      # 6. Tracks mit SCDL herunterladen
      - name: Tracks herunterladen
        run: |
          scdl_command="scdl -l '${{ github.event.inputs.url }}' --download-archive '${{ env.sync_file }}' --path '${{ env.download_path }}' --hide-progress"
          echo "SCDL-Befehl wird ausgeführt:"
          echo "$scdl_command"
          eval "$scdl_command"

      # 7. Tracks in Videos umwandeln
      - name: Tracks in Videos umwandeln
        run: |
          echo "Starte die Umwandlung von Tracks in Videos..."
          for track in "${{ env.download_path }}"/*.mp3; do
            if [ -f "$track" ]; then
              # Name des Videos basierend auf dem Tracknamen
              video_name=$(basename "$track" .mp3).mp4
              video_path="${{ env.video_output_path }}/$video_name"

              # FFmpeg-Befehl zur Erstellung des Videos
              ffmpeg -loop 1 -i "${{ env.stock_image }}" -i "$track" -c:v libx264 -c:a aac -b:a 192k -shortest "$video_path"

              echo "Video erstellt: $video_path"
            fi
          done

      # 8. Videos in das Repository übernehmen und commiten
      - name: Videos commiten
        run: |
          git config user.name "${{ github.actor }}"
          git config user.email "${{ github.actor }}@users.noreply.github.com"
          git add "${{ env.video_output_path }}/*.mp4"
          git commit -m "Neue Videos aus heruntergeladenen Tracks erstellt"
          git push
