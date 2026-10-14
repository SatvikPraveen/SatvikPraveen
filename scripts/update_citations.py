#!/usr/bin/env python3
"""Refresh the Google Scholar citation count shown by the README badge.

Usage:  python3 scripts/update_citations.py

Reads the total citation count from the public Scholar profile and writes
Assets/citations.json in the shields.io endpoint format. If Scholar blocks
the request or the page layout changes, the script exits non-zero and leaves
the existing JSON untouched, so the badge keeps its last good value.
"""
import json, os, re, sys, urllib.request

SCHOLAR_ID = "BMr6EWAAAAAJ"
URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "Assets", "citations.json")

def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def main():
    try:
        html = fetch()
    except Exception as e:
        sys.exit(f"fetch failed: {e}")
    # The stats table lists citations (all, since year), h-index, i10-index;
    # the first gsc_rsb_std cell is total citations.
    cells = re.findall(r'class="gsc_rsb_std">(\d+)<', html)
    if not cells:
        sys.exit("citation count not found (blocked or page layout changed)")
    count = int(cells[0])

    badge = {"schemaVersion": 1, "label": "Citations", "message": str(count),
             "color": "4285F4", "namedLogo": "googlescholar", "logoColor": "white",
             "style": "flat-square", "cacheSeconds": 3600}
    with open(OUT, "w") as f:
        json.dump(badge, f, indent=2)
        f.write("\n")
    print(f"citations: {count}")

if __name__ == "__main__":
    main()
