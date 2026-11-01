#!/usr/bin/env bash
# Creates a working copy of a pret decompilation with this game's changes
# applied, ready to edit and build.
#
#   ./setup.sh <firered-leafgreen|ruby-sapphire|emerald> [checkout dir]
#
# The decomp is cloned at the commit listed in games.txt (default location:
# work/<repository>), <Folder>/source/phys-spec-split.diff is applied on top,
# and pret's agbcc compiler is built and installed into it. Needs git, make,
# a C compiler, libpng and arm-none-eabi-binutils (see README.md).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GAME="${1:-}"
line=$(awk -v g="$GAME" '$1 == g && g != "agbcc"' "$HERE/games.txt")
[ -n "$line" ] || { echo "usage: $0 <firered-leafgreen|ruby-sapphire|emerald> [checkout dir]"; exit 1; }
read -r _ folder repo commit <<< "$line"
DEST="${2:-$HERE/work/$repo}"
[ ! -e "$DEST" ] || { echo "error: $DEST already exists"; exit 1; }

echo "== cloning pret/$repo at $commit"
git clone -q "https://github.com/pret/$repo.git" "$DEST"
git -C "$DEST" -c advice.detachedHead=false checkout -q "$commit"
git -C "$DEST" apply --binary "$HERE/$folder/source/phys-spec-split.diff"
mkdir -p "$DEST/patches"

# agbcc is shared between checkouts and only built once
AGBCC="$HERE/work/agbcc"
if [ ! -x "$AGBCC/agbcc" ]; then
    read -r _ _ _ agbcc_commit <<< "$(awk '$1 == "agbcc"' "$HERE/games.txt")"
    echo "== building pret/agbcc at $agbcc_commit"
    rm -rf "$AGBCC"
    git clone -q https://github.com/pret/agbcc.git "$AGBCC"
    git -C "$AGBCC" -c advice.detachedHead=false checkout -q "$agbcc_commit"
    (cd "$AGBCC" && ./build.sh > build.log 2>&1) || { tail -20 "$AGBCC/build.log"; exit 1; }
fi
(cd "$AGBCC" && ./install.sh "$DEST" > /dev/null)
echo "== ready: $DEST"
