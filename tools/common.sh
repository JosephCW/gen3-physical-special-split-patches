# Shared setup for the scripts in tools/. Source it after setting USAGE.
#
# Takes the game name ($1: firered-leafgreen, ruby-sapphire or emerald) and sets:
#   ROOT    this repository        FOLDER  the game's folder, e.g. $ROOT/Emerald
#   SRC     the working copy: $SRC_DIR if set, otherwise work/<decomp>
# plus everything in the game's game.conf (DECOMP, COMMIT, TARGETS, ...).
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGBCC_COMMIT=da598c1d918402c42c0c0d7128ba14567f3175e9   # pret/agbcc
MGBA="${MGBA:-/Applications/mGBA.app/Contents/MacOS/mGBA}"

case "${1:-}" in
    firered-leafgreen) FOLDER="$ROOT/FireRed-LeafGreen" ;;
    ruby-sapphire)     FOLDER="$ROOT/Ruby-Sapphire" ;;
    emerald)           FOLDER="$ROOT/Emerald" ;;
    *) echo "usage: $USAGE"; exit 1 ;;
esac
GAME="$1"
. "$FOLDER/game.conf"
SRC="${SRC_DIR:-$ROOT/work/$DECOMP}"

# The ROM a make target builds (from TARGETS)
built_rom() {
    awk -v t="$1" '$1 == t {print $3}' <<< "$TARGETS"
}

# Copy the working copy to $1 with every build output and generated file
# removed, keeping the installed compiler, so old build files can't leak in.
clean_copy() {
    rsync -a --exclude /build --exclude '/*.gba' --exclude '/*.elf' "$SRC/" "$1/"
    (cd "$1" && git clean -fdXq)
    rsync -a "$SRC/tools/agbcc/" "$1/tools/agbcc/"
}
