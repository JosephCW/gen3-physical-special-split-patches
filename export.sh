#!/usr/bin/env bash
# Copies your changes from a working copy back into this repository: writes
# <Folder>/source/phys-spec-split.diff and copies the rebuilt .bps patches.
# Run it after patch_tools/make_patches.sh.
#
#   ./export.sh <firered-leafgreen|ruby-sapphire|emerald> [checkout dir]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GAME="${1:-}"
line=$(awk -v g="$GAME" '$1 == g && g != "agbcc"' "$HERE/games.txt")
[ -n "$line" ] || { echo "usage: $0 <firered-leafgreen|ruby-sapphire|emerald> [checkout dir]"; exit 1; }
read -r _ folder repo commit <<< "$line"
SRC="$(cd "${2:-$HERE/work/$repo}" && pwd)"
[ "$(git -C "$SRC" rev-parse HEAD)" = "$commit" ] || { echo "error: $SRC is not at $commit (see games.txt)"; exit 1; }

# Stage everything into a throwaway index, so the checkout's own index is
# untouched. patches/ is left out: the .bps files are copied separately.
INDEX="$(mktemp)"
trap 'rm -f "$INDEX"' EXIT
export GIT_INDEX_FILE="$INDEX"
git -C "$SRC" read-tree HEAD
git -C "$SRC" add -A -- . ':!patches' ':!**/__pycache__/**'
git -C "$SRC" add -f patch_tools/visual_test/harness.diff   # matched by pret's *.diff ignore rule
mkdir -p "$HERE/$folder/source"
git -C "$SRC" diff --cached --binary --full-index HEAD > "$HERE/$folder/source/phys-spec-split.diff"
unset GIT_INDEX_FILE

cp "$SRC"/patches/*.bps "$HERE/$folder/"
echo "== $folder: wrote source/phys-spec-split.diff ($(grep -c '^diff --git' "$HERE/$folder/source/phys-spec-split.diff") files) and copied $(ls "$SRC"/patches/*.bps | wc -l | tr -d ' ') patches"
