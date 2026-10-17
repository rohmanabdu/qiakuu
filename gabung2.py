import requests, re, os

SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"
SOURCE_3 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama3.m3u" # SOURCE 3 TAMBAHAN
OUTPUT_FILE = "derama/hasil.m3u"
ONE_CATEGORY = "LIVE EVENT"

def get_raw(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"GAGAL ambil {url}: {e}")
        return ""

r1 = get_raw(SOURCE_1)
r2 = get_raw(SOURCE_2)
r3 = get_raw(SOURCE_3) # AMBIL SOURCE 3

# Hapus header #EXTM3U di source 2 dan 3 biar tidak double
r2_no_head = re.sub(r'^#EXTM3U.*\n', '', r2, count=1, flags=re.MULTILINE)
r3_no_head = re.sub(r'^#EXTM3U.*\n', '', r3, count=1, flags=re.MULTILINE)

# Gabung 3 source
combined = r1.rstrip() + "\n" + r2_no_head.strip() + "\n" + r3_no_head.strip() + "\n"

# Ganti semua group-title jadi satu kategori
final = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', combined)

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final)

print(f"Selesai {final.count('#EXTINF')} channel dari 3 source -> {OUTPUT_FILE}")
