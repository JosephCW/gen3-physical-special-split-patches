# Pokémon Emerald: Physical/Special Split patch

This patch gives Pokémon Emerald the **Gen 4 physical/special split**. Each move is
Physical, Special or Status based on what the move is, not on its type, using its
Diamond/Pearl/Platinum category. The game also **shows each move's category in-game**.

![Category icons (top) next to Emerald's Fight / Water / Steel icons (bottom)](screenshots/category_icons_closeup.png)

> **Other games:** see the [overview](../README.md) for FireRed/LeafGreen,
> Ruby/Sapphire and Emerald.

## Compatible game

| Patch file | Use it on | CRC32 | SHA-1 |
|---|---|---|---|
| `Emerald_PhysSpecSplit.bps` | **Pokémon Emerald Version (USA, Europe)**, game code `BPEE` | `1F1C08FB` | `f3ae088181bf583e55daf962a92bb46f4f1d07b7` |

* The ROM must be a **clean, unmodified, English (USA, Europe)** Emerald dump. Emerald
  has only one English revision. The patch does **not** work on other languages or on a
  ROM that's already patched or hacked. BPS patches check the original ROM's checksum, so
  a patcher will refuse the wrong ROM.
* The patch doesn't change the save format, so **existing Emerald saves keep working**.
  Back up your `.sav` first anyway.

## How to apply the patch

Choose any of these:

**Rom Patcher JS (browser, any OS):**
1. Open <https://www.marcrobledo.com/RomPatcher.js/>.
2. *ROM file*: choose your clean Emerald `.gba`.
3. *Patch file*: choose `Emerald_PhysSpecSplit.bps` from this folder.
4. Click **Apply patch** and save the new `.gba`.

**Floating IPS (Flips), Windows/Linux:**
1. Open Flips and click **Apply Patch**.
2. Select the `.bps`, then your clean ROM, then choose where to save the patched ROM.

**mGBA soft-patching (no new file is written):**
* Put the `.bps` next to the ROM with the **same file name**, e.g.
  `Pokemon Emerald.gba` + `Pokemon Emerald.bps`. mGBA applies it on load.
* Or from a terminal: `mGBA -p Emerald_PhysSpecSplit.bps "Pokemon Emerald.gba"`.

**Command line (Python 3, included here):**
```sh
python3 ../bps.py apply "Pokemon Emerald.gba" Emerald_PhysSpecSplit.bps "Emerald Split.gba"
```

Then play the patched `.gba` in any GBA emulator or on a flash cart.

## What you'll see in-game

**Summary screen → BATTLE MOVES → press A on a move.** A PHYS / SPEC / STATUS badge appears
at the right end of the DESCRIPTION header, next to the move's description and POWER /
ACCURACY. This is also the screen you get when you **learn a new move by level-up or TM
with four moves already known**, so you can see the new move's category before you choose
a move to forget. The badge isn't shown on the CONTEST MOVES page.

| Special | Physical | Status |
|---|---|---|
| ![](screenshots/summary_flamethrower_special.png) | ![](screenshots/summary_slash_physical.png) | ![](screenshots/summary_scary_face_status.png) |

| Learning a new move (Earthquake) | Shadow Ball is now Special |
|---|---|
| ![](screenshots/learn_new_move_earthquake_physical.png) | ![](screenshots/summary_shadow_ball_special.png) |

**Move Relearner** (Fallarbor Town): the BATTLE MOVES panel has a new third row with the
category, under the type and PP.

| Physical | Status | Special |
|---|---|---|
| ![](screenshots/move_relearner_scratch_physical.png) | ![](screenshots/move_relearner_growl_status.png) | ![](screenshots/move_relearner_ember_special.png) |

**Bag → TMs & HMs pocket:** the selected TM/HM's type and category are shown stacked in the
empty space beside the bag (they hide on CLOSE BAG and in the other pockets).

| Status | Physical | Special |
|---|---|---|
| ![](screenshots/bag_tm_toxic_status.png) | ![](screenshots/bag_tm_earthquake_physical.png) | ![](screenshots/bag_tm_flamethrower_special.png) |

(The screenshots were rendered from the emulator's video memory by the visual test below.)

## What changed in battle

* Each move has a category (`split`) taken from its Gen 4 category.
* Damage uses **Attack/Defense for Physical moves and Sp. Atk/Sp. Def for Special moves**,
  whatever the move's type. Reflect, Light Screen, burn, Guts, Hustle, Huge/Pure Power,
  Choice Band, crits that ignore stat stages, etc. all follow the category.
* **Counter** reflects Physical hits and **Mirror Coat** reflects Special hits.
* Type-boosting held items (Charcoal, Mystic Water, …) boost the stat that matches the
  move's category.
* Hidden Power and Weather Ball are always Special (as in Gen 4), whatever their type.
* The Battle Frontier TV "Battle Seminar" show scores Reflect/Light Screen by the
  attacking move's category too.

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

* The category isn't shown in the battle move menu. Check a move's category from the party
  summary screen or the Bag's TMs & HMs pocket.
* A few of the enemy AI's move-scoring hints still use the old type-based idea of
  physical/special, e.g. whether a Defense- or Sp. Def-raising move is worth using against
  your Pokémon's types. This only slightly changes which moves the AI likes to pick.
  Damage is always calculated correctly.

---

# Updating or modifying the patch

The patch is built from the [pret/pokeemerald](https://github.com/pret/pokeemerald)
decompilation, which builds a byte-identical Emerald ROM. This repository stores the changes as `source/phys-spec-split.diff`, against the upstream
commit listed in [`games.txt`](../games.txt). To change the patch, make a working copy of
the decomp with the changes applied, edit the C source there, rebuild, and export the
result back here.

## Files changed

[`source/phys-spec-split.diff`](source/phys-spec-split.diff) has every change (or run
`git diff` in your working copy). In brief:

| File | Change |
|---|---|
| `include/pokemon.h` | `SPLIT_PHYSICAL` / `SPLIT_SPECIAL` / `SPLIT_STATUS` constants and a new `u8 split;` field in `struct BattleMove` (uses existing padding; still 12 bytes per move) |
| `src/data/battle_moves.h` | `.split = SPLIT_…,` added to every move |
| `include/battle.h` | `IS_MOVE_PHYSICAL(move)` / `IS_MOVE_SPECIAL(move)` replace the old type-based macros |
| `src/pokemon.c` | `CalculateBaseDamage` picks stats by the move's category |
| `src/battle_script_commands.c` | Hustle accuracy, Counter/Mirror Coat damage tracking |
| `src/battle_tv.c` | Battle Seminar Reflect/Light Screen scoring |
| `graphics/types/split_physical.png`, `split_special.png`, `split_status.png` | the three badges (new files, 32×16, same palettes as the type icons) |
| `graphics_file_rules.mk` | appends the badges to the type-icon sprite sheet |
| `src/pokemon_summary_screen.c` | badge sprite (`SPRITE_ARR_ID_SPLIT`, `SpriteCB_SplitIcon`), shown while battle move details are open (`splitIconMove`) |
| `src/menu_specialized.c` | Move Relearner: rows moved up 8 px and a category row added (`MoveRelearnerLoadBattleMoveDescription`) |
| `include/pokemon_summary_screen.h` | shares the move type icon sprite sheet/animations/palette map (`gSpriteSheet_MoveTypes` etc.) with the bag |
| `src/item_menu.c`, `include/item_menu.h` | Bag TMs & HMs pocket: type + category icons (`LoadTmIconGfx`, `CreateTmIconSprites`, `SpriteCB_TmIcon`; selected move kept in `gBagMenu->tmMove`) |
| `patch_tools/` | patch builder, BPS tool, and visual test (below) |

## Common edits

* **Change a move's category:** edit its `.split` in `src/data/battle_moves.h`, e.g.
  ```c
  [MOVE_BITE] = { ..., .split = SPLIT_PHYSICAL, },
  ```
* **Change the badge art:** edit `graphics/types/split_*.png`. Keep them 32×16 indexed
  PNGs using the type-icon palettes (`move_types_1.pal` for PHYS/STATUS, `move_types_2.pal`
  for SPEC; see `sMoveTypeToOamPaletteNum`).
* **Move the badge on screen:** change `SPLIT_ICON_X` / `SPLIT_ICON_Y` at the top of
  `pokemon_summary_screen.c`, or `TM_ICON_X` / `TM_ICON_Y` in `item_menu.c` for the Bag.
* **Rename the relearner text:** `sText_SplitPhysical` etc. in `menu_specialized.c`.

## One-time setup (macOS)

From the top of this repository:
```sh
brew install arm-none-eabi-gcc arm-none-eabi-binutils libpng pkgconf
./setup.sh emerald
```
This clones [pret/pokeemerald](https://github.com/pret/pokeemerald) at the pinned commit into
`work/pokeemerald`, applies `source/phys-spec-split.diff`, and builds and installs pret's
agbcc compiler. `work/` is ignored by git. (For Linux or Windows/WSL packages, see the
decomp's `INSTALL.md`.)

## Rebuild the patch

```sh
cd work/pokeemerald
patch_tools/make_patches.sh ~/Downloads/"Pokemon - Emerald Version (USA, Europe).gba"
```

The script checks the ROM's SHA-1 and rejects anything that isn't a clean Emerald. It then
runs `make`, writes `patches/Emerald_PhysSpecSplit.bps`, and confirms the patch rebuilds
the modified ROM exactly. The ROMs are built in a fresh temporary copy of the source with every build output and
generated graphic removed, so nothing left over from earlier builds can end up in a patch. The built ROM is also copied to
`pokeemerald.gba` in the repository root if you want to play it directly.

Then copy your source changes and the new patches back into this repository:
```sh
../../export.sh emerald
```
This rewrites `source/phys-spec-split.diff` and copies the `.bps` files into this folder.
Commit both.

To check that the original game still builds byte-for-byte (for example after updating
the decomp), build the untouched upstream code in a separate checkout. Your changes and
build files aren't affected:
```sh
cd work/pokeemerald
git worktree add --detach /tmp/vanilla-check HEAD
cp -R tools/agbcc /tmp/vanilla-check/tools/
make -C /tmp/vanilla-check -j8 compare
git worktree remove --force /tmp/vanilla-check
```

## Visual test (optional)

```sh
patch_tools/visual_test/run_visual_test.sh
```

This builds a throwaway copy of the game with `harness.diff` applied. The copy plays
itself to NEW GAME, opens the summary screen, the forget-a-move screen and the Move
Relearner, and writes PNGs of each screen to `patch_tools/visual_test/out/`. It uses the
[mGBA](https://mgba.io) app (`brew install --cask mgba-app`) and its GDB stub. An mGBA
window opens for a minute or two while it runs. Your real source tree isn't changed. (The Bag
screenshots came from a variant of the same harness that opens the TMs & HMs pocket instead.)

To update the README screenshots, copy the PNGs you want from
`patch_tools/visual_test/out/` into this folder's `screenshots/`.

## Credits

* [pret/pokeemerald](https://github.com/pret/pokeemerald) decompilation and
  [pret/agbcc](https://github.com/pret/agbcc).
* Move categories are from Generation 4, checked against Pokémon Showdown's move data.
