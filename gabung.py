import requests, re, os

SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/deqiaa/refs/heads/main/playlist_final.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"
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
        if not s: continue
        if s.startswith("#EXTINF"):
            # simpan block sebelumnya jika ada
            if cur_extinf:
                blocks.append((cur_extinf, cur_props, "")) # gak ada url, skip nanti
            cur_extinf = s
            cur_props = []
        elif s.startswith("#") and cur_extinf:
            cur_props.append(s)
        elif s.startswith("http") and cur_extinf:
            blocks.append((cur_extinf, cur_props, s))
            cur_extinf = None
            cur_props = []
    return blocks

r1 = get_raw(SOURCE_1)
r2 = get_raw(SOURCE_2)

b1 = parse_blocks(r1)
b2 = parse_blocks(r2)

print(f"SOURCE 1 ketemu: {len(b1)} block")
print(f"SOURCE 2 ketemu: {len(b2)} block")

all_blocks = b1 + b2
final_lines = ["#EXTM3U"]
for extinf, props, url in all_blocks:
    if not url: continue
    # ganti group-title
    extinf = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', extinf)
    if 'group-title=' not in extinf:
        extinf = extinf.replace(',', f' group-title="{ONE_CATEGORY}",', 1)
    
    final_lines.append(extinf)
    # LOGIKA UNTUK APK KAMU:
    if ".mpd" in url.lower():
        # untuk MPD wajib ada ini biar ExoPlayer di APK mau play
        has_manifest = any("manifest_type" in p for p in props)
        if not has_manifest:
            final_lines.append("#KODIPROP:inputstream.adaptive.manifest_type=mpd")
        # pertahankan props yang lain kalau ada license
        for p in props:
            if "KODIPROP" in p or "EXTVLCOPT" in p:
                final_lines.append(p)
    # kalau m3u8, jangan pakai KODIPROP biar ringan
    final_lines.append(url)

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(final_lines) + "\n")

print(f"Selesai TOTAL {len(final_lines)//2} channel -> {OUTPUT_FILE}")
