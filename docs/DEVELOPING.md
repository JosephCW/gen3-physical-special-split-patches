# Developing the patches

How the patches are built from source, how to change them, and how they're tested. For
what the patches do and how to apply them, see the [main README](../README.md).

## How it fits together

The patches are built from [pret](https://github.com/pret)'s decompilations, which compile
to byte-identical ROMs. This repository doesn't contain the decomps. Each game folder holds
only what this project adds:

| Path | What it is |
|---|---|
| `<Game>/source/phys-spec-split.diff` | every change to the game's source, against a pinned upstream commit |
| `<Game>/game.conf` | the decomp, the pinned commit, the `make` targets and the patch each one produces, and test settings |
| `<Game>/tests/harness.diff` | test-only code for the [visual test](#visual-test) (never in a patch) |
| `<Game>/tests/test_ai.inc` | test-only code for the [AI test](#ai-test) (never in a patch) |
| `<Game>/*.bps`, `<Game>/screenshots/`, `<Game>/README.md` | the patches, screenshots and game-specific notes |
| `tools/` | the scripts below, shared by all three games |
| `work/` | working copies made by `tools/setup.sh` (ignored by git) |

| Games | Decomp | Name used by the scripts |
|---|---|---|
| FireRed / LeafGreen | [pret/pokefirered](https://github.com/pret/pokefirered) | `firered-leafgreen` |
| Ruby / Sapphire | [pret/pokeruby](https://github.com/pret/pokeruby) | `ruby-sapphire` |
| Emerald | [pret/pokeemerald](https://github.com/pret/pokeemerald) | `emerald` |

Each game's README lists the files its diff changes and the common edits (changing a move's
category, the badge art or position, …).

## Prerequisites

On macOS:
```sh
brew install arm-none-eabi-gcc arm-none-eabi-binutils libpng pkgconf
brew install --cask mgba-app        # only for the visual and AI tests
```
For Linux or Windows/WSL, install the packages listed in the decomp's `INSTALL.md`. The
tests look for mGBA at `/Applications/mGBA.app`; set `MGBA=/path/to/mGBA` to use another.

## Changing a patch

Run everything from the top of this repository. Emerald is the example; use
`firered-leafgreen` or `ruby-sapphire` for the others.

```sh
tools/setup.sh emerald                                  # working copy in work/pokeemerald
# ... edit the source in work/pokeemerald ...
tools/make_patches.sh emerald "/path/to/clean Emerald.gba"   # rebuild Emerald/*.bps
tools/export.sh emerald                                 # save your edits to Emerald/source/
```

* **`setup.sh`** clones the decomp at the commit in `game.conf`, applies
  `source/phys-spec-split.diff`, and builds and installs pret's agbcc compiler (built once,
  in `work/agbcc`).
* **`make_patches.sh`** takes one or more clean ROMs in any order. It identifies each by its
  SHA-1, builds the matching target in a fresh copy of the working copy (so leftover build
  files can't end up in a patch), writes the `.bps` into the game folder, and checks that
  the patch recreates the built ROM exactly. The built ROM is also copied into the working
  copy if you want to play it.
* **`export.sh`** writes the working copy's changes back to `source/phys-spec-split.diff`.

Commit the diff and the `.bps` files together. To use a working copy somewhere other than
`work/`, set `SRC_DIR=/path/to/it` for any of the scripts.

## Building without the scripts

The same steps by hand, using Emerald as the example. Take the decomp, commit and `make`
target from the game's `game.conf`.

```sh
# 1. pret's agbcc compiler
git clone https://github.com/pret/agbcc
cd agbcc && git checkout da598c1d918402c42c0c0d7128ba14567f3175e9 && ./build.sh && cd ..

# 2. the decomp at the pinned commit, with this repository's changes applied
git clone https://github.com/pret/pokeemerald
cd pokeemerald
git checkout 731ad5bfd6e6f265508d0efcca0ba42f9dcf5881
git apply --binary /path/to/gen3/Emerald/source/phys-spec-split.diff
(cd ../agbcc && ./install.sh ../pokeemerald)

# 3. build the modified ROM
make -j8                            # Emerald; e.g. `make firered_rev1` or `make ruby_rev2` for others

# 4. make the patch from your clean ROM and the built ROM, with any BPS tool
python3 /path/to/gen3/tools/bps.py create "clean Emerald.gba" pokeemerald.gba Emerald_PhysSpecSplit.bps
#   or: flips --create --bps "clean Emerald.gba" pokeemerald.gba Emerald_PhysSpecSplit.bps
```

To save source edits by hand, write the diff from the decomp's directory (`git add -N`
makes new files show up in it):
```sh
git add -N . && git diff --binary --full-index HEAD > /path/to/gen3/Emerald/source/phys-spec-split.diff
```

## Checking the original game still builds

After changing the pinned commit, build the untouched upstream code in a separate checkout
and compare it with the official ROM. Each game's README lists its `compare` targets.
```sh
cd work/pokeemerald
git worktree add --detach /tmp/vanilla-check HEAD
cp -R tools/agbcc /tmp/vanilla-check/tools/
make -C /tmp/vanilla-check -j8 compare
git worktree remove --force /tmp/vanilla-check
```

## Visual test

```sh
tools/visual_test/run_visual_test.sh emerald [make target]
```

This produced the README screenshots. They aren't emulator screen captures: they're
rendered from the game's own video memory by a self-driving test build, so they show the
GBA's own graphics at native resolution.

1. The script copies the working copy to a temporary folder and applies the game's
   `tests/harness.diff`. This adds code that skips the intro, builds a test party (a
   Charizard with Flamethrower, Slash, Scary Face and Shadow Ball), and presses buttons on
   a fixed schedule to open the changed screens.
2. It builds that copy and runs it in [mGBA](https://mgba.io) with mGBA's GDB stub turned on.
3. `gdb_dump.py`, a small GDB Remote Serial Protocol client (plain Python, no gdb needed),
   connects to mGBA on port 2345, stops the game at each screen, and dumps VRAM, palette
   RAM, sprite (OAM) memory and the display registers. `arm-none-eabi-nm` finds the
   addresses to stop at.
4. `render_gba.py` redraws the four tiled background layers and the sprites from each dump
   into a PNG. It's a simple software renderer: it skips colour blending, windows and
   sprite scaling, which these menus barely use.

The harness also runs a damage check (Bite, Shadow Ball, Fire Punch and Flamethrower from
an Attack-200 / Sp. Atk-50 attacker), which confirms damage follows each move's category.

| Game | Default target | Screens |
|---|---|---|
| FireRed / LeafGreen | `leafgreen` | summary, forget-a-move, Move Relearner |
| Ruby / Sapphire | `ruby_rev2` | summary, forget-a-move, Move Tutor |
| Emerald | `all` | summary, forget-a-move, Move Relearner |

The PNGs go to `tools/visual_test/out/<game>/` (ignored by git); copy the ones you want
into the game's `screenshots/` folder. The TM Case and Bag screenshots came from a variant
of the harness whose button schedule opens the TM Case or the Bag's TMs & HMs pocket
instead. An mGBA window opens for a minute or two. Your working copy isn't changed.

The category badges were drawn to match each game's art: FireRed/LeafGreen's are added to
the menu icon sheet `graphics/interface/menu_info.png`, and Ruby/Sapphire/Emerald's are made
from the Fight, Water and Steel type icons, using the same palettes.

## AI test

```sh
tools/ai_test/run_ai_test.sh emerald [make target]
```

This produced the [Trainer AI](../README.md#trainer-ai) table. It builds the game twice:
from the untouched upstream code ("before") and from your working copy ("after"), each
with the game's `tests/test_ai.inc` added. That code runs at boot: it sets up a battle
state for each scenario (the target's types, Attack / Sp. Atk and last move, and the AI's
four moves), runs the AI's move-scoring script 256 times with a fixed random seed, and
sums the scores. `ai_read.py` reads the sums from each build in mGBA over the GDB stub,
and `ai_report.py` prints the table. Default targets: `firered`, `ruby_rev2` and `all`.
Like the visual test, it doesn't change your working copy.
