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

def extract_channels(text):
    # Ambil semua pola #EXTINF sampai URL di bawahnya, ini yang bikin semua channel ketarik
    pattern = r'#EXTINF:.*\n.*'
    return re.findall(pattern, text, re.IGNORECASE)

r1 = get_raw(SOURCE_1)
r2 = get_raw(SOURCE_2)

ch1 = extract_channels(r1)
ch2 = extract_channels(r2)

print(f"SOURCE 1 ketemu: {len(ch1)} channel")
print(f"SOURCE 2 ketemu: {len(ch2)} channel")

all_channels = ch1 + ch2

# Ganti semua group-title jadi LIVE EVENT dan susun ulang bersih
final_channels = []
for ch in all_channels:
    fixed = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', ch)
    # Kalau belum ada group-title, tambahin
    if 'group-title=' not in fixed:
        fixed = fixed.replace('#EXTINF:', f'#EXTINF: group-title="{ONE_CATEGORY}" ', 1) if 'group-title' not in fixed else fixed
        # fix double group-title
        fixed = re.sub(r'group-title="[^"]*".*?group-title', f'group-title="{ONE_CATEGORY}"', fixed)
    final_channels.append(fixed)

final_content = "#EXTM3U\n" + "\n".join(final_channels) + "\n"

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"Selesai TOTAL {len(final_channels)} channel -> {OUTPUT_FILE}")
