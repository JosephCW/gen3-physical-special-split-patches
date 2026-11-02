#!/usr/bin/env bash
# Creates a working copy of a pret decompilation with this game's changes
# applied, ready to edit, build and test.
#
#   tools/setup.sh <firered-leafgreen|ruby-sapphire|emerald>
#
# Clones the decomp at the commit in <Game>/game.conf into work/<decomp> (or
# $SRC_DIR), applies <Game>/source/phys-spec-split.diff, and builds and installs
# pret's agbcc compiler. Needs git, make, a C compiler, libpng and
# arm-none-eabi-binutils (see docs/DEVELOPING.md).
set -euo pipefail
USAGE="$0 <firered-leafgreen|ruby-sapphire|emerald>"
. "$(dirname "$0")/common.sh"
[ ! -e "$SRC" ] || { echo "error: $SRC already exists"; exit 1; }

echo "== cloning pret/$DECOMP at $COMMIT"
git clone -q "https://github.com/pret/$DECOMP.git" "$SRC"
git -C "$SRC" -c advice.detachedHead=false checkout -q "$COMMIT"
git -C "$SRC" apply --binary "$FOLDER/source/phys-spec-split.diff"

# agbcc is shared between working copies and only built once
AGBCC="$ROOT/work/agbcc"
if [ ! -x "$AGBCC/agbcc" ]; then
    echo "== building pret/agbcc at $AGBCC_COMMIT"
    rm -rf "$AGBCC"
    git clone -q https://github.com/pret/agbcc.git "$AGBCC"
    git -C "$AGBCC" -c advice.detachedHead=false checkout -q "$AGBCC_COMMIT"
    (cd "$AGBCC" && ./build.sh > build.log 2>&1) || { tail -20 "$AGBCC/build.log"; exit 1; }
fi
(cd "$AGBCC" && ./install.sh "$SRC" > /dev/null)
echo "== ready: $SRC"
