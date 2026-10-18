import requests, re, os

SOURCE = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/playlist_final.m3u"
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

def parse_all_categories(text):
    blocks = []
    lines = text.splitlines()
    cur_extinf = None
    cur_props = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#EXTINF"):
            if cur_extinf:
                blocks.append((cur_extinf, cur_props, ""))
            cur_extinf = s
            cur_props = []
        elif s.startswith("#") and cur_extinf:
            cur_props.append(s)
        elif s.startswith("http") and cur_extinf:
            blocks.append((cur_extinf, cur_props, s))
            cur_extinf = None
            cur_props = []
    return blocks

raw = get_raw(SOURCE)
blocks = parse_all_categories(raw)

# Hitung kategori asli biar keliatan
live_now = 0
up_coming = 0
other = 0
for extinf, _, _ in blocks:
    low = extinf.lower()
    if "live now" in low or "live_now" in low:
        live_now += 1
    elif "up coming" in low or "up_coming" in low or "upcoming" in low:
        up_coming += 1
    else:
        other += 1

print(f"TOTAL DARI SOURCE: {len(blocks)} channel")
print(f"- LIVE NOW: {live_now}")
print(f"- UP COMING: {up_coming}")
print(f"- LAINNYA: {other}")

final_lines = ["#EXTM3U"]
count = 0
for extinf, props, url in blocks:
    if not url:
        continue
    
    # Jadikan semua jadi 1 kategori biar tampil semua di APK
    extinf = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', extinf)
    if 'group-title=' not in extinf:
        extinf = extinf.replace(',', f' group-title="{ONE_CATEGORY}",', 1)

    final_lines.append(extinf)
    
    # Biar semua MPD tampil di APK ExoPlayer
    if ".mpd" in url.lower():
        if not any("manifest_type" in p for p in props):
            final_lines.append("#KODIPROP:inputstream.adaptive.manifest_type=mpd")
        for p in props:
            if "KODIPROP" in p:
                final_lines.append(p)
    else:
        for p in props:
            if "EXTVLCOPT" in p:
                final_lines.append(p)

    final_lines.append(url)
    count += 1

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(final_lines) + "\n")

print(f"Selesai -> {count} channel (LIVE NOW + UP COMING) semua masuk ke {OUTPUT_FILE}")
