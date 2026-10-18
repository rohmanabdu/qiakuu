import requests
import os

SOURCE = "https://bandeltv.xyz/2026/vid/New.php"
VIDEO_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/upcoming.mp4"
VIDEO_LAMA = "waitng_event_gemini.mp4"

# folder output
OUTPUT_DIR = "derama"
OUTPUT_M3U = f"{OUTPUT_DIR}/hasil.m3u"
OUTPUT_JSON = f"{OUTPUT_DIR}/hasil.json"

r = requests.get(SOURCE, timeout=15, headers={
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://bandeltv.xyz/"
})
raw = r.text

print(f"Panjang source: {len(raw)}")
print(f"Apakah upcoming? {VIDEO_LAMA in raw}")

# JANGAN PARSE JSON, LANGSUNG GANTI STRING SAJA
final = raw.replace(
    "https://bandeltv.xyz/film/waitng_event_gemini.mp4", VIDEO_CUSTOM
).replace(
    "https://bandeltv.xyz/film/waitng_event_gemini.mp4".replace("https","http"), VIDEO_CUSTOM
).replace(VIDEO_LAMA, VIDEO_CUSTOM)

# bikin folder derama otomatis kalau belum ada
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Simpan ke folder derama
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    f.write(final)

with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write(final)

print(f"[✓] {OUTPUT_JSON} disimpan")
print(f"[✓] {OUTPUT_M3U} disimpan TANPA UBAH STRUKTUR")
