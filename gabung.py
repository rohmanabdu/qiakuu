import requests, re, os
SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"
OUTPUT_FILE = "derama/hasil.m3u"
ONE_CATEGORY = "LIVE EVENT"

def get_raw(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    return r.text

r1 = get_raw(SOURCE_1)
r2 = get_raw(SOURCE_2)
r2_no_head = re.sub(r'^#EXTM3U.*\n', '', r2, count=1, flags=re.MULTILINE)
combined = r1.rstrip() + "\n" + r2_no_head.strip() + "\n"
final = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', combined)
os.makedirs("derama", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final)
print(f"Selesai {final.count('#EXTINF')} channel")
