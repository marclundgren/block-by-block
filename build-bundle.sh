#!/usr/bin/env bash
# Build the sellable artifacts into dist/:
#   block-by-block.html  (linear, print-styled)
#   block-by-block.pdf   (via headless chromium in docker)
#   block-by-block.epub  (via pandoc in docker)
#   block-by-block-projects.zip  (the project files in bundle/)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist

echo "1/4 linear HTML"; python3 build-book.py

echo "2/4 EPUB"; docker run --rm -v "$PWD/dist":/d pandoc/core \
  /d/block-by-block.html -f html -t epub3 -o /d/block-by-block.epub \
  --metadata title="Block by Block" --metadata author="Marc Lundgren" \
  --metadata lang=en --toc --toc-depth=1

echo "3/4 PDF"; docker run --rm -v "$PWD/dist":/d --entrypoint chromium-browser zenika/alpine-chrome \
  --no-sandbox --headless --disable-gpu --hide-scrollbars --no-pdf-header-footer \
  --virtual-time-budget=30000 --print-to-pdf=/d/block-by-block.pdf file:///d/block-by-block.html

echo "4/4 project zip"
for proj in realtime-time-sync autorun-toggle; do
  rm -rf "bundle/$proj"; mkdir -p "bundle/$proj"
  (cd "$HOME/Dev/$proj" && git archive --format=tar HEAD) | tar -x -C "bundle/$proj"
done
python3 -c "import shutil; shutil.make_archive('dist/block-by-block-projects','zip','bundle')"

docker run --rm -v "$PWD/dist":/d alpine chown -R "$(id -u):$(id -g)" /d 2>/dev/null || true
echo "done -> dist/"
ls -la dist/
