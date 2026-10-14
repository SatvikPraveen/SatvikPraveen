#!/bin/bash
# Refresh the citation badge from this machine and push it.
#
# Google Scholar refuses requests from GitHub's runners, so the count is
# fetched locally (a macOS launch agent runs this weekly). The script only
# touches Assets/citations.json, and steps aside when the checkout has other
# work in progress so it never commits or overwrites anything else.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

if [ "$(git symbolic-ref --short HEAD)" != "main" ] || [ -n "$(git status --porcelain)" ]; then
    echo "skipped: checkout is not a clean main"
    exit 0
fi

git pull --ff-only --quiet origin main
/usr/bin/python3 scripts/update_citations.py

if git diff --quiet -- Assets/citations.json; then
    echo "no change"
    exit 0
fi
git add Assets/citations.json
git commit --quiet -m "Update citation count"
git push --quiet origin main
echo "pushed"
