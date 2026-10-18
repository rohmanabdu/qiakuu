import requests, os, sys

SOURCE = "https://bandeltv.xyz/2026/vid/New.php"
OUTPUT_DIR = "derama"
OUTPUT_M3U = f"{OUTPUT_DIR}/hasil.m3u"
OUTPUT_JSON = f"{OUTPUT_DIR}/hasil.json"

VIDEO_LAMA = "waitng_event_gemini.mp4"
VIDEO_CUSTOM = "https://raw.githubusercontent.com/rohmanabdu/cloudd/main/upcoming.mp4"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://bandeltv.xyz/",
    "Origin": "https://bandeltv.xyz"
}

try:
    r = requests.get(SOURCE, timeout=30, headers=headers)
    raw = r.text
except Exception as e:
    print(f"[X] Request gagal: {e}")
    sys.exit(0)

print(f"Panjang source: {len(raw)}")

# kalau ke-block kayak kemarin, jangan timpa file lama
if "Gagal mengambil URL" in raw or "cURL Error" in raw or len(raw) < 1000:
    print("[X] Source ke-block, STOP biar gak ngerusak file lama")
    sys.exit(0)

final = raw.replace("https://bandeltv.xyz/film/waitng_event_gemini.mp4", VIDEO_CUSTOM).replace(VIDEO_LAMA, VIDEO_CUSTOM)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# INI KUNCINYA, BIKIN 2 FILE SEKALIGUS
with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
    f.write(final)

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    f.write(final)

print(f"[✓] {OUTPUT_M3U} ada")
print(f"[✓] {OUTPUT_JSON} ada")
