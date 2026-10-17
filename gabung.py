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

def parse_blocks(text):
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
blocks = parse_blocks(raw)

print(f"SOURCE ketemu: {len(blocks)} channel")

final_lines = ["#EXTM3U"]
count = 0
for extinf, props, url in blocks:
    if not url:
        continue
    
    # Paksa semua group-title jadi LIVE EVENT
    extinf = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', extinf)
    if 'group-title=' not in extinf:
        extinf = extinf.replace(',', f' group-title="{ONE_CATEGORY}",', 1)

    final_lines.append(extinf)
    
    # Biar APK ExoPlayer mau baca semua MPD
    if ".mpd" in url.lower():
        has_manifest = any("manifest_type" in p for p in props)
        if not has_manifest:
            final_lines.append("#KODIPROP:inputstream.adaptive.manifest_type=mpd")
        # Pertahankan semua license biar gak ke-skip di APK
        for p in props:
            if "KODIPROP" in p:
                final_lines.append(p)
    else:
        # Kalau m3u8, pertahankan VLCOPT kalau ada
        for p in props:
            if "EXTVLCOPT" in p:
                final_lines.append(p)

    final_lines.append(url)
    count += 1

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(final_lines) + "\n")

print(f"Selesai TOTAL {count} channel tampil semua -> {OUTPUT_FILE}")
