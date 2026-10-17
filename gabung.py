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

def extract_channels_full(text):
    channels = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            # ambil semua baris # yang ada di bawah EXTINF (VLCOPT, KODIPROP, dll) sampai ketemu URL
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    i += 1
                    continue
                if nxt.startswith("#") and not nxt.startswith("#EXTINF"):
                    block.append(nxt)
                    i += 1
                else:
                    # ini URL nya
                    if nxt.startswith("http"):
                        block.append(nxt)
                    i += 1
                    break
            channels.append("\n".join(block))
        else:
            i += 1
    return channels

r1 = get_raw(SOURCE_1)
r2 = get_raw(SOURCE_2)

ch1 = extract_channels_full(r1)
ch2 = extract_channels_full(r2)

print(f"SOURCE 1 ketemu: {len(ch1)} channel")
print(f"SOURCE 2 ketemu: {len(ch2)} channel")

all_channels = ch1 + ch2

final_channels = []
for ch in all_channels:
    fixed = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', ch)
    final_channels.append(fixed)

final_content = "#EXTM3U\n" + "\n".join(final_channels) + "\n"

os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"Selesai TOTAL {len(final_channels)} channel -> {OUTPUT_FILE}")
