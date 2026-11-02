#!/usr/bin/env bash
# Measures how the trainer AI scores Reflect, Light Screen, Growl, Counter and
# Mirror Coat in a few fixed situations, before and after this patch.
#
#   tools/ai_test/run_ai_test.sh <firered-leafgreen|ruby-sapphire|emerald> [make target]
#
# Builds two throwaway copies of the game: "before" is the untouched upstream
# code, "after" is the working copy. Both get the game's tests/test_ai.inc,
# which runs the AI's scoring script many times at boot. Each copy runs in mGBA
# with the GDB stub, ai_read.py reads the scores, and ai_report.py prints a
# before/after table. The working copy is not changed.
set -euo pipefail
USAGE="$0 <firered-leafgreen|ruby-sapphire|emerald> [make target]"
. "$(dirname "$0")/../common.sh"
HERE="$ROOT/tools/ai_test"
TARGET="${2:-$AI_TARGET}"
ROM="$(built_rom "$TARGET")"
[ -n "$ROM" ] || { echo "error: unknown target $TARGET (see game.conf)"; exit 1; }
WORK="$(mktemp -d)"
MGBA_PID=""
trap 'kill $MGBA_PID 2>/dev/null || true; rm -rf "$WORK"' EXIT

mkdir "$WORK/before"
git -C "$SRC" archive HEAD | tar -x -C "$WORK/before"
rsync -a "$SRC/tools/agbcc/" "$WORK/before/tools/agbcc/"
clean_copy "$WORK/after"
for tree in before after; do
    cd "$WORK/$tree"
    cp "$FOLDER/tests/test_ai.inc" src/
    # Include the test after main.c's last #include, and run it before the main loop
    python3 -I - src/main.c <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
last = [m.end() for m in re.finditer(r'^#include .*$', s, re.M)][-1]
s = s[:last] + '\n#include "test_ai.inc"' + s[last:]
assert s.count('\n    for (;;)\n') == 1
s = s.replace('\n    for (;;)\n', '\n    TestAi();\n    for (;;)\n')
open(p, 'w').write(s)
PY
    echo "== building $tree"
    make -j8 "$TARGET" > build.log 2>&1 || { tail -20 build.log; exit 1; }
    ELF="${ROM%.gba}.elf"
    BP=$(arm-none-eabi-nm "$ELF" | awk '$3=="TestAiDone"{print $1}')
    SCORES=$(arm-none-eabi-nm "$ELF" | awk '$3=="gTestAiScore"{print $1}')
    "$MGBA" -g "$ROM" > /dev/null 2>&1 &
    MGBA_PID=$!
    python3 -I "$HERE/ai_read.py" "$BP" "$SCORES" > "$WORK/$tree.txt"
    kill $MGBA_PID; wait $MGBA_PID 2>/dev/null || true; MGBA_PID=""
done
python3 -I "$HERE/ai_report.py" "$WORK/before.txt" "$WORK/after.txt"
