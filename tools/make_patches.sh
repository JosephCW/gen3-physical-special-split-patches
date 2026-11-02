#!/usr/bin/env bash
# Builds the modified ROMs from a working copy and writes the .bps patches into
# the game's folder.
#
#   tools/make_patches.sh <firered-leafgreen|ruby-sapphire|emerald> <clean ROM> [<clean ROM> ...]
#
# Each clean ROM is identified by its SHA-1 (checked against the decomp's
# *.sha1 files), and the matching target from the game's game.conf is built.
# The build runs in a fresh copy of the working copy with every build output
# removed, so leftovers from earlier builds can never end up in a patch. Each
# patch is checked to recreate the built ROM exactly, and the built ROM is also
# copied to the working copy for playing.
set -euo pipefail
USAGE="$0 <firered-leafgreen|ruby-sapphire|emerald> <clean ROM> [...]"
. "$(dirname "$0")/common.sh"
shift
[ $# -ge 1 ] || { echo "usage: $USAGE"; exit 1; }
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
echo "== copying $SRC to a clean build directory"
clean_copy "$WORK/repo"

for clean in "$@"; do
    have=$(shasum "$clean" | cut -d' ' -f1)
    found=""
    while read -r target sha_file built out; do
        [ -n "$target" ] || continue
        [ "$(cut -d' ' -f1 "$WORK/repo/$sha_file")" = "$have" ] || continue
        found=1
        echo "== $clean is $target; building"
        make -C "$WORK/repo" -j8 "$target" > "$WORK/build.log" 2>&1 || { tail -20 "$WORK/build.log"; exit 1; }
        cp "$WORK/repo/$built" "$SRC/$built"
        python3 -I "$ROOT/tools/bps.py" create "$clean" "$WORK/repo/$built" "$FOLDER/$out"
        # Make sure the patch recreates the built ROM exactly
        python3 -I "$ROOT/tools/bps.py" apply "$clean" "$FOLDER/$out" "$WORK/verify.gba"
        cmp "$WORK/repo/$built" "$WORK/verify.gba"
        echo "== $FOLDER/$out OK"
    done <<< "$TARGETS"
    [ -n "$found" ] || { echo "error: $clean is not a supported clean ROM (sha1 $have)"; exit 1; }
done
