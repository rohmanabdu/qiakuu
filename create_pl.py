# Daftar URL dari luar (bisa link dari repo lain / github)
SEGMENTS = [
    "https://github.com/aderandi/diktaads/raw/refs/heads/main/DiktaTVGratis_M3U8/segment_000.ts",
    "https://github.com/aderandi/diktaads/raw/refs/heads/main/DiktaTVGratis_M3U8/segment_001.ts",
]

# Folder output
FOLDER = "PL"
OUTPUT = f"{FOLDER}/defira.m3u"

import os
os.makedirs(FOLDER, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for i, url in enumerate(SEGMENTS, start=1):
        f.write(f"#EXTINF:-1,Dikta TV Gratis {i}\n")
        f.write(f"{url}\n")

print(f"Berhasil buat {OUTPUT} dengan {len(SEGMENTS)} channel")
