name: Gabung Playlist
on: [workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Download 2 playlist
        run: |
          curl -L -o rama1.m3u "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
          curl -L -o rama2.m3u "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"
          echo "rama1:" $(grep -c "#EXTINF" rama1.m3u)
          echo "rama2:" $(grep -c "#EXTINF" rama2.m3u)

      - name: Gabung - Logo Original Tetap, Kategori Jadi 1
        run: |
          mkdir -p derama
          # Gabung file mentah
          cat rama1.m3u > gabungan_raw.m3u
          grep -v "^#EXTM3U" rama2.m3u >> gabungan_raw.m3u
          
          # HANYA ganti group-title, JANGAN sentuh tvg-logo
          sed 's/group-title="[^"]*"/group-title="LIVE EVENT"/g' gabungan_raw.m3u > derama/hasil.m3u
          
          # Kalau ada yang belum punya group-title, tambahkan
          sed -i 's/#EXTINF:-1 /#EXTINF:-1 group-title="LIVE EVENT" /g' derama/hasil.m3u
          sed -i 's/#EXTINF:-1,/#EXTINF:-1 group-title="LIVE EVENT",/g' derama/hasil.m3u
          
          echo "TOTAL HASIL:" $(grep -c "#EXTINF" derama/hasil.m3u)
          head -20 derama/hasil.m3u

      - name: Push
        run: |
          git config --global user.name "bot"
          git config --global user.email "bot@bot.com"
          git add derama/hasil.m3u
          git commit -m "gabung logo original semua channel" || true
          git push
