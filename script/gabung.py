import requests, re, os

SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"

OUTPUT_FILE = "derama/hasil.m3u"
ONE_CATEGORY = "LIVE EVENT"
DEFAULT_LOGO = "https://img.magnific.com/premium-vector/live-streaming-icon-live-broadcasting-button-online-stream-icon_349999-1413.jpg"

def get_m3u(url):
    print(f"Ambil: {url}")
    r = requests.get(url, timeout=40, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def parse_and_clean(text):
    channels = []
    lines = text.splitlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            # PAKSA jadi 1 kategori + paksa logo
            line = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', line)
            if 'group-title=' not in line:
                line = line.replace(',', f' group-title="{ONE_CATEGORY}",', 1)

            line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{DEFAULT_LOGO}"', line)
            if 'tvg-logo=' not in line:
                line = line.replace('#EXTINF:-1', f'#EXTINF:-1 tvg-logo="{DEFAULT_LOGO}"')

            if i+1 < len(lines):
                url = lines[i+1].strip()
                if url.startswith("http"):
                    channels.append((line, url))
    return channels

def main():
    # INI YANG BIKIN ERROR TADI, SEKARANG SUDAH FIX
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    list1 = parse_and_clean(get_m3u(SOURCE_1))
    list2 = parse_and_clean(get_m3u(SOURCE_2))

    print(f"Sumber 1: {len(list1)}")
    print(f"Sumber 2: {len(list2)}")

    unique = {}
    for extinf, url in list1 + list2:
        if url not in unique:
            unique[url] = extinf

    print(f"Total gabungan: {len(unique)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for url, extinf in unique.items():
            f.write(f"{extinf}\n{url}\n")

    print(f"SELESAI -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
