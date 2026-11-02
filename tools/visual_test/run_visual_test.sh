#!/usr/bin/env bash
# Builds a throwaway, self-driving copy of the modified game that opens the
# changed screens, runs it in mGBA with the GDB stub, and renders a PNG of each
# screen into tools/visual_test/out/<game>/. The working copy is not changed.
#
#   tools/visual_test/run_visual_test.sh <firered-leafgreen|ruby-sapphire|emerald> [make target]
#
# The game's tests/harness.diff adds the code that plays itself to the screens;
# game.conf says which target to build by default and how many screens it captures.
set -euo pipefail
USAGE="$0 <firered-leafgreen|ruby-sapphire|emerald> [make target]"
. "$(dirname "$0")/../common.sh"
HERE="$ROOT/tools/visual_test"
TARGET="${2:-$VISUAL_TARGET}"
ROM="$(built_rom "$TARGET")"
[ -n "$ROM" ] || { echo "error: unknown target $TARGET (see game.conf)"; exit 1; }
OUT="$HERE/out/$GAME"
WORK="$(mktemp -d)"
MGBA_PID=""
trap 'kill $MGBA_PID 2>/dev/null || true; rm -rf "$WORK"' EXIT

clean_copy "$WORK/repo"
cd "$WORK/repo"
git apply "$FOLDER/tests/harness.diff"
make -j8 "$TARGET" > build.log 2>&1 || { tail -20 build.log; exit 1; }

ELF="${ROM%.gba}.elf"
BP=$(arm-none-eabi-nm "$ELF" | awk '$3=="TestDumpPoint"{print $1}')
REGS=$(arm-none-eabi-nm "$ELF" | awk -v s="$VISUAL_REGS" '$3==s{print $1}')
"$MGBA" -g "$ROM" > /dev/null 2>&1 &
MGBA_PID=$!
rm -rf "$OUT"
python3 -I "$HERE/gdb_dump.py" "$BP" "$OUT" "$VISUAL_DUMPS" "$REGS"
for f in "$OUT"/*.bin; do
    python3 -I "$HERE/render_gba.py" "$f" "${f%.bin}.png"
    rm "$f"
done
echo "Screens written to $OUT/"
