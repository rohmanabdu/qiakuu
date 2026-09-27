import requests, re, os

SOURCE_1 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama1.m3u"
SOURCE_2 = "https://raw.githubusercontent.com/rohmanabdu/lian/refs/heads/main/playlist/rama2.m3u"
OUTPUT_FILE = "derama/hasil.m3u"
ONE_CATEGORY = "LIVE EVENT"

def get_raw(url):
    print(f"Ambil: {url}")
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    return r.text

def force_one_category_only(m3u_text):
    # Hanya ganti group-title="..." -> group-title="LIVE EVENT"
    # JANGAN SENTUH tvg-logo sama sekali
    text = re.sub(r'group-title="[^"]*"', f'group-title="{ONE_CATEGORY}"', m3u_text)
    # Kalau ada channel yang belum punya group-title, tambahkan
    text = re.sub(r'(#EXTINF:-1[^\n,]*),', f'\\1 group-title="{ONE_CATEGORY}",', text)
    # Hapus duplikat group-title kalau jadi double karena line di atas
    text = re.sub(f'group-title="{ONE_CATEGORY}"\\s+group-title="{ONE_CATEGORY}"', f'group-title="{ONE_CATEGORY}"', text)
    return text

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    raw1 = get_raw(SOURCE_1)
    raw2 = get_raw(SOURCE_2)

    print(f"RAW1 panjang: {len(raw1)} char")
    print(f"RAW2 panjang: {len(raw2)} char")

    # Bersihkan header #EXTM3U dari file kedua biar cuma 1 header
    raw2_no_header = re.sub(r'^#EXTM3U.*\n', '', raw2, count=1, flags=re.MULTILINE)

    combined = raw1.rstrip() + "\n" + raw2_no_header.strip() + "\n"

    # Sekarang baru paksa 1 kategori, logo tetap original
    final = force_one_category_only(combined)

    # Hitung berapa siaran
    count = final.count("#EXTINF")
    print(f"Total siaran yang akan ditulis: {count}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"SELESAI -> {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
