# Pokémon FireRed & LeafGreen: Physical/Special Split patch

This patch gives Pokémon FireRed and LeafGreen the **Gen 4 physical/special split**. Each move is
Physical, Special or Status based on what the move is, not on its type, using its
Diamond/Pearl/Platinum category. The game also **shows each move's category in-game**
with a PHYS / SPEC / STATUS badge.

![Category icons](screenshots/category_icons_closeup.png)

> **Other games:** see the [overview](../README.md) for FireRed/LeafGreen,
> Ruby/Sapphire and Emerald.

## Compatible games

| Patch file | Use it on | CRC32 | SHA-1 |
|---|---|---|---|
| `FireRed_PhysSpecSplit_v1.0.bps` | **Pokémon FireRed Version (USA) v1.0**, game code `BPRE`, revision 0 | `DD88761C` | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `FireRed_PhysSpecSplit_v1.1.bps` | **Pokémon FireRed Version (USA) v1.1 (Rev 1)**, game code `BPRE`, revision 1 | `84EE4776` | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `LeafGreen_PhysSpecSplit_v1.0.bps` | **Pokémon LeafGreen Version (USA) v1.0**, game code `BPGE`, revision 0 | `D69C96CC` | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `LeafGreen_PhysSpecSplit_v1.1.bps` | **Pokémon LeafGreen Version (USA) v1.1 (Rev 1)**, game code `BPGE`, revision 1 | `DAFFECEC` | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

* Use the **FireRed** patches on FireRed and the **LeafGreen** patches on LeafGreen. They
  aren't interchangeable.
* The ROM must be a **clean, unmodified, English (USA)** dump. The patches do **not**
  work on European or Japanese versions, or on a ROM that's already patched or hacked.
* Not sure which revision you have? Try the v1.0 patch for your game first. BPS patches check the
  original ROM's checksum, so a patcher will refuse the wrong one (for example "source
  checksum mismatch"). If it does, use the v1.1 patch. You can also compare your ROM's
  CRC32 with the table (Rom Patcher JS shows it), or its SHA-1 (`shasum rom.gba`).
* The patch doesn't change the save format, so **existing FireRed/LeafGreen
  saves keep working**. Back up your `.sav` first anyway.

## How to apply the patch

Choose any of these:

**Rom Patcher JS (browser, any OS):**
1. Open <https://www.marcrobledo.com/RomPatcher.js/>.
2. *ROM file*: choose your clean FireRed or LeafGreen `.gba`.
3. *Patch file*: choose the matching `.bps` from this folder.
4. Click **Apply patch** and save the new `.gba`.

**Floating IPS (Flips), Windows/Linux:**
1. Open Flips and click **Apply Patch**.
2. Select the `.bps`, then your clean ROM, then choose where to save the patched ROM.

**mGBA soft-patching (no new file is written):**
* Put the `.bps` next to the ROM with the **same file name**, e.g.
  `Pokemon FireRed.gba` + `Pokemon FireRed.bps`. mGBA applies it on load.
* Or from a terminal: `mGBA -p FireRed_PhysSpecSplit_v1.0.bps "Pokemon FireRed.gba"`.

**Command line (Python 3, included here):**
```sh
python3 ../bps.py apply "Pokemon FireRed.gba" FireRed_PhysSpecSplit_v1.0.bps "FireRed Split.gba"
```

Then play the patched `.gba` in any GBA emulator or on a flash cart.

## What you'll see in-game

**Summary screen → Moves → press A on a move.** The badge sits to the right of the POWER
box. This is also the screen you get when you **learn a new move by level-up or TM with
four moves already known**, so you can see the new move's category before you choose a
move to forget.

| Special | Physical | Status |
|---|---|---|
| ![](screenshots/summary_flamethrower_special.png) | ![](screenshots/summary_slash_physical.png) | ![](screenshots/summary_scary_face_status.png) |

| Learning a new move (Earthquake) | Shadow Ball is now Special |
|---|---|
| ![](screenshots/learn_new_move_earthquake_physical.png) | ![](screenshots/summary_shadow_ball_special.png) |

**Move Relearner** (Two Island move tutor): the badge appears under the ACCURACY label.

| Special | Physical | Status |
|---|---|---|
| ![](screenshots/move_relearner_heat_wave_special.png) | ![](screenshots/move_relearner_scratch_physical.png) | ![](screenshots/move_relearner_growl_status.png) |

**TM Case:** the first row of the move info box shows the type and category side by side
(in place of the old "TYPE" label).

| Status | Physical | Special |
|---|---|---|
| ![](screenshots/tm_case_toxic_status.png) | ![](screenshots/tm_case_earthquake_physical.png) | ![](screenshots/tm_case_flamethrower_special.png) |

(The screenshots are from LeafGreen; FireRed looks the same. They were rendered from the
emulator's video memory by the visual test below.)

## What changed in battle

* Each move has a category (`split`) taken from its Gen 4 category.
* Damage uses **Attack/Defense for Physical moves and Sp. Atk/Sp. Def for Special moves**,
  whatever the move's type. Reflect, Light Screen, burn, Guts, Hustle, Huge/Pure Power,
  Choice Band, crits that ignore stat stages, etc. all follow the category.
* **Counter** reflects Physical hits and **Mirror Coat** reflects Special hits.
* Type-boosting held items (Charcoal, Mystic Water, …) boost the stat that matches the
  move's category.
* Hidden Power and Weather Ball are always Special (as in Gen 4), whatever their type.

**28 moves are now Physical** (were Special): Fire Punch, Ice Punch, Thunder Punch, Vine
Whip, Bite, Razor Leaf, Waterfall, Clamp, Crabhammer, Thief, Flame Wheel, Faint Attack,
Outrage, Spark, Sacred Fire, Pursuit, Crunch, Beat Up, Knock Off, Dive, Blaze Kick, Ice
Ball, Needle Arm, Bullet Seed, Icicle Spear, Dragon Claw, Volt Tackle, Leaf Blade.

**26 moves are now Special** (were Physical): Razor Wind, Gust, Sonic Boom, Acid, Hyper
Beam, Night Shade, Smog, Sludge, Swift, Tri Attack, Snore, Aeroblast, Sludge Bomb, Mud
Slap, Hidden Power, Ancient Power, Shadow Ball, Uproar, Spit Up, Hyper Voice, Weather
Ball, Air Cutter, Silver Wind, Signal Beam, Mud Shot, Doom Desire.

Every other move keeps the category it already had.

### Known limitations

* The badge isn't shown in the battle move menu. Check a move's category from the party
  summary screen or the TM Case.
* A few of the enemy AI's move-scoring hints still use the old type-based idea of
  physical/special, e.g. whether a Defense- or Sp. Def-raising move is worth using against
  your Pokémon's types. This only slightly changes which moves the AI likes to pick. Damage is always
  calculated correctly.

---

# Updating or modifying the patch

The patch is built from the [pret/pokefirered](https://github.com/pret/pokefirered)
decompilation, which builds byte-identical FireRed and LeafGreen ROMs. Both games share
the same source, so one set of changes covers all four patches. This repository stores the changes as `source/phys-spec-split.diff`, against the upstream
commit listed in [`games.txt`](../games.txt). To change the patch, make a working copy of
the decomp with the changes applied, edit the C source there, rebuild, and export the
result back here.

## Files changed

[`source/phys-spec-split.diff`](source/phys-spec-split.diff) has every change (or run
`git diff` in your working copy). In brief:

| File | Change |
|---|---|
| `include/constants/pokemon.h` | `SPLIT_PHYSICAL` / `SPLIT_SPECIAL` / `SPLIT_STATUS` constants |
| `include/pokemon.h` | new `u8 split;` field in `struct BattleMove` (uses existing padding; still 12 bytes per move) |
| `src/data/battle_moves.h` | `.split = SPLIT_…,` added to every move |
| `include/battle.h` | `IS_MOVE_PHYSICAL(move)` / `IS_MOVE_SPECIAL(move)` replace the old type-based macros |
| `src/pokemon.c` | `CalculateBaseDamage` picks stats by the move's category |
| `src/battle_script_commands.c` | Hustle accuracy, Counter/Mirror Coat damage tracking |
| `graphics/interface/menu_info.png` | PHYS / SPEC / STATUS badges added to the top row (x = 32, 64, 96) |
| `include/menu.h`, `src/list_menu.c` | `MENU_INFO_ICON_PHYSICAL/SPECIAL/STATUS` icon IDs |
| `src/pokemon_summary_screen.c` | draws the badge in `PokeSum_PrintSelectedMoveStats` |
| `src/learn_move.c` | new window 8 + badge in `PrintMoveInfo` (Move Relearner) |
| `src/tm_case.c` | TM Case: "TYPE" label dropped; type + category badges on the first row (`DrawMoveInfoLabels`, `PrintMoveInfo`) |
| `patch_tools/` | patch builder, BPS tool, and visual test (below) |

## Common edits

* **Change a move's category:** edit its `.split` in `src/data/battle_moves.h`, e.g.
  ```c
  [MOVE_BITE] = { ..., .split = SPLIT_PHYSICAL, },
  ```
* **Change the badge art:** edit `graphics/interface/menu_info.png`. Keep it an indexed
  PNG and draw in the top row using the existing palette's second row (indices 16–31).
  Each badge is 32×12. The build converts it automatically.
* **Move the badge on screen:** change the `x, y` passed to `BlitMenuInfoIcon` in
  `pokemon_summary_screen.c` / `learn_move.c` / `tm_case.c`.

## One-time setup (macOS)

From the top of this repository:
```sh
brew install arm-none-eabi-gcc arm-none-eabi-binutils libpng pkgconf
./setup.sh firered-leafgreen
```
This clones [pret/pokefirered](https://github.com/pret/pokefirered) at the pinned commit into
`work/pokefirered`, applies `source/phys-spec-split.diff`, and builds and installs pret's
agbcc compiler. `work/` is ignored by git. (For Linux or Windows/WSL packages, see the
decomp's `INSTALL.md`.)

## Rebuild the patches

Pass whichever clean ROMs you have, from the list in "Compatible games", in any order:

```sh
cd work/pokefirered
patch_tools/make_patches.sh ~/Downloads/"Pokemon - FireRed Version (USA).gba" "/path/to/LeafGreen v1.0.gba"
```

The script identifies each ROM by its SHA-1 and rejects anything that isn't a clean
supported ROM. It then builds the matching game (`make firered`, `firered_rev1`,
`leafgreen` or `leafgreen_rev1`), writes the `.bps` into `patches/`, and confirms the
patch rebuilds the modified ROM exactly. Only the patches for the ROMs you pass are
rebuilt. The ROMs are built in a fresh temporary copy of the source with every build output and
generated graphic removed, so nothing left over from earlier builds can end up in a patch. The built ROMs are also copied to the repository root
(`pokefirered.gba`, `pokeleafgreen.gba`, …) if you want to play them directly.

Then copy your source changes and the new patches back into this repository:
```sh
../../export.sh firered-leafgreen
```
This rewrites `source/phys-spec-split.diff` and copies the `.bps` files into this folder.
Commit both.

To check that the original game still builds byte-for-byte (for example after updating
the decomp), build the untouched upstream code in a separate checkout. Your changes and
build files aren't affected:
```sh
cd work/pokefirered
git worktree add --detach /tmp/vanilla-check HEAD
cp -R tools/agbcc /tmp/vanilla-check/tools/
make -C /tmp/vanilla-check -j8 compare_firered
make -C /tmp/vanilla-check -j8 compare_leafgreen
git worktree remove --force /tmp/vanilla-check
```

## Visual test (optional)

```sh
patch_tools/visual_test/run_visual_test.sh            # LeafGreen
patch_tools/visual_test/run_visual_test.sh firered    # FireRed
```

This builds a throwaway copy of the game with `harness.diff` applied. The copy plays
itself to NEW GAME, opens the summary screen, the forget-a-move screen and the Move
Relearner, and writes PNGs of each screen to `patch_tools/visual_test/out/`. (The TM Case
screenshots came from a variant of the same harness that opens the TM Case instead.) It uses the
[mGBA](https://mgba.io) app (`brew install --cask mgba-app`) and its GDB stub. An mGBA
window opens for a minute or two while it runs. Your real source tree isn't changed.

To update the README screenshots, copy the PNGs you want from
`patch_tools/visual_test/out/` into this folder's `screenshots/`.

## Credits

* [pret/pokefirered](https://github.com/pret/pokefirered) decompilation and
  [pret/agbcc](https://github.com/pret/agbcc).
* Move categories are from Generation 4, checked against Pokémon Showdown's move data.
