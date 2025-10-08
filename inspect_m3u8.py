import os, sys
from urllib.parse import urljoin, urlparse
import requests

# رابط m3u8 المراد فحصه
URL = "https://uvotv-aniview.global.ssl.fastly.net/hls/live/2119033/slntv/playlist.m3u8"
UA = "Mozilla/5.0"

def resolve_lines(base_url, text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            out.append(line)
            continue
        if s.startswith("http://") or s.startswith("https://"):
            out.append(s)
        else:
            out.append(urljoin(base_url, s))
    return "\n".join(out)

def main():
    print(f"[i] Fetching: {URL}")
    r = requests.get(URL, timeout=20, headers={"User-Agent": UA})
    r.raise_for_status()
    text = r.text
    print("\n=== Preview (first 30 lines) ===")
    print("\n".join(text.splitlines()[:30]))
    print("=== End Preview ===\n")

    # استنتاج الـ Base URL
    base = URL.rsplit("/", 1)[0] + "/"
    print(f"[i] Guessed Base URL: {base}")

    resolved = resolve_lines(base, text)
    with open("resolved_playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(resolved)
    print("[i] File written: resolved_playlist.m3u8")

if __name__ == "__main__":
    main()
