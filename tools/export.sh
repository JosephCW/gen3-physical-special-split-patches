#!/usr/bin/env bash
# Saves the source changes in a working copy back into this repository as
# <Game>/source/phys-spec-split.diff. Run it after editing the source.
#
#   tools/export.sh <firered-leafgreen|ruby-sapphire|emerald>
set -euo pipefail
USAGE="$0 <firered-leafgreen|ruby-sapphire|emerald>"
. "$(dirname "$0")/common.sh"
[ "$(git -C "$SRC" rev-parse HEAD)" = "$COMMIT" ] || { echo "error: $SRC is not at $COMMIT (see game.conf)"; exit 1; }

# Stage everything into a throwaway index, so the working copy's own index is
# untouched, and diff it against the upstream commit.
INDEX="$(mktemp)"
trap 'rm -f "$INDEX"' EXIT
export GIT_INDEX_FILE="$INDEX"
git -C "$SRC" read-tree HEAD
git -C "$SRC" add -A
git -C "$SRC" diff --cached --binary --full-index HEAD > "$FOLDER/source/phys-spec-split.diff"
echo "== wrote $FOLDER/source/phys-spec-split.diff ($(grep -c '^diff --git' "$FOLDER/source/phys-spec-split.diff") files)"
