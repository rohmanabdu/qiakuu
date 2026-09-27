import requests, re, os

SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"

OUTPUT_FILE = "derama/hasil.m3u"
ONE_CATEGORY = "LIVE EVENT"

def get_m3u(url):
    print(f"Ambil: {url}")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    return r.text

def parse_keep_logo(text):
    """Ambil EXTINF original apa adanya, cuma ganti group-title saja"""
    channels = []
    lines = text.splitlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            # Cuma ganti group-title, JANGAN sentuh tvg-logo sama sekali
            if 'group-title=' in line:
                new_line = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', line)
            else:
                # kalau gak ada group-title, sisipkan
                new_line = line.replace(',', f' group-title="{ONE_CATEGORY}",', 1)

            # cari url di baris selanjutnya
            for j in range(i+1, len(lines)):
                url = lines[j].strip()
                if url:
                    if url.startswith("http"):
                        channels.append((new_line, url))
                    break
    return channels

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    data1 = get_m3u(SOURCE_1)
    data2 = get_m3u(SOURCE_2)

    list1 = parse_keep_logo(data1)
    list2 = parse_keep_logo(data2)

    print(f"rama1: {len(list1)} siaran")
    print(f"rama2: {len(list2)} siaran")

    # GABUNG SEMUA TANPA HAPUS DUPLIKAT BIAR SEMUA TAMPIL
    gabungan = list1 + list2

    print(f"Total akan ditulis: {len(gabungan)} siaran (semua kebawa)")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for extinf, url in gabungan:
            f.write(f"{extinf}\n{url}\n")

    print(f"SELESAI -> {OUTPUT_FILE} - Logo original, semua siaran kebawa")

if __name__ == "__main__":
    main()
