name: Gabung M3U

on:
  schedule:
    - cron: '*/15 * * * *'  # jalan tiap 1 jam, jangan 15 menit biar gak kena limit GitHub
  workflow_dispatch:      # bisa jalanin manual
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install requests
        run: pip install requests

      - name: Jalankan gabung.py
        run: python gabung.py

      - name: Commit hasil.m3u
        run: |
          git config --global user.name "bot"
          git config --global user.email "bot@github.com"
          git add derama/hasil.m3u
          git diff --staged --quiet || git commit -m "update hasil.m3u"
          git push
