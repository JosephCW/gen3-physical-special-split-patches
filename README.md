# Gen 3 Physical/Special Split patches

These patches give the Game Boy Advance Pokémon games the **Gen 4 physical/special split**.
Each move is Physical, Special or Status based on the move itself, not its type. They also
show each move's category in-game: on the summary screen, when learning a move, at the
Move Relearner/Tutor, and in the TM Case or Bag.

Find your ROM below, open that game's folder, and follow its README.

| Your ROM (clean, English) | Folder | Patch file | ROM CRC32 |
|---|---|---|---|
| FireRed (USA) v1.0 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md) | `FireRed_PhysSpecSplit_v1.0.bps` | `DD88761C` |
| FireRed (USA) v1.1 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md) | `FireRed_PhysSpecSplit_v1.1.bps` | `84EE4776` |
| LeafGreen (USA) v1.0 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md) | `LeafGreen_PhysSpecSplit_v1.0.bps` | `D69C96CC` |
| LeafGreen (USA) v1.1 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md) | `LeafGreen_PhysSpecSplit_v1.1.bps` | `DAFFECEC` |
| Ruby (USA, Europe) v1.0 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Ruby_PhysSpecSplit_v1.0.bps` | `F0815EE7` |
| Ruby (USA, Europe) Rev 1 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Ruby_PhysSpecSplit_v1.1.bps` | `61641576` |
| Ruby (USA, Europe) Rev 2 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Ruby_PhysSpecSplit_v1.2.bps` | `AEAC73E6` |
| Sapphire (USA, Europe) v1.0 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Sapphire_PhysSpecSplit_v1.0.bps` | `554DEDC4` |
| Sapphire (USA, Europe) Rev 1 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Sapphire_PhysSpecSplit_v1.1.bps` | `BAFEDAE5` |
| Sapphire (USA, Europe) Rev 2 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md) | `Sapphire_PhysSpecSplit_v1.2.bps` | `9CC4410E` |
| Emerald (USA, Europe) | [`Emerald/`](Emerald/README.md) | `Emerald_PhysSpecSplit.bps` | `1F1C08FB` |

Not sure which revision you have? Try the patches for that game one at a time in a BPS
patcher (e.g. [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)). BPS patches
check the ROM's checksum, so only the right one will apply. Other languages and
already-hacked ROMs aren't supported.

`bps.py` in this folder applies a patch from the command line (Python 3):
```sh
python3 bps.py apply "Pokemon Emerald.gba" Emerald/Emerald_PhysSpecSplit.bps "Emerald Split.gba"
```

## Building from source

The patches are built from pret's decompilations of the games, which compile to
byte-identical ROMs. Each game folder stores its changes as `source/phys-spec-split.diff`
against a pinned upstream commit, listed in [`games.txt`](games.txt):

| Games | Decomp | Diff |
|---|---|---|
| FireRed / LeafGreen | [pret/pokefirered](https://github.com/pret/pokefirered) | [`FireRed-LeafGreen/source/`](FireRed-LeafGreen/source/phys-spec-split.diff) |
| Ruby / Sapphire | [pret/pokeruby](https://github.com/pret/pokeruby) | [`Ruby-Sapphire/source/`](Ruby-Sapphire/source/phys-spec-split.diff) |
| Emerald | [pret/pokeemerald](https://github.com/pret/pokeemerald) | [`Emerald/source/`](Emerald/source/phys-spec-split.diff) |

To modify a patch (macOS; see each decomp's `INSTALL.md` for Linux/WSL packages):

```sh
brew install arm-none-eabi-gcc arm-none-eabi-binutils libpng pkgconf
./setup.sh emerald                  # or firered-leafgreen / ruby-sapphire
cd work/pokeemerald                 # edit the source here, then:
patch_tools/make_patches.sh "/path/to/clean Emerald.gba"
../../export.sh emerald             # copy the diff and new .bps back into Emerald/
```

`setup.sh` clones the decomp at the pinned commit into `work/`, applies the diff, and
builds pret's agbcc compiler. `export.sh` writes your changes back as the diff and copies
the rebuilt patches. Each game's README has the details: the files changed, common edits,
and a visual test that screenshots the new UI in mGBA.

## Repository layout

| Path | What it is |
|---|---|
| `<Game>/*.bps` | the patches |
| `<Game>/README.md` | compatibility, how to apply, screenshots, what changed, how to modify |
| `<Game>/source/phys-spec-split.diff` | every source change, including the build and test tools under `patch_tools/` |
| `games.txt` | pinned upstream commits of the decomps and agbcc |
| `setup.sh`, `export.sh` | create a working copy with the changes / save changes back |
| `bps.py` | command-line BPS patcher (create and apply) |

## License

The patches, scripts and source changes in this repository are released under the
[MIT License](LICENSE). This repository contains no ROMs or game data: you need your
own clean ROM. Pokémon is © Nintendo, Creatures Inc. and GAME FREAK inc.; this project
is not affiliated with or endorsed by them. The decompilations are the work of
[pret](https://github.com/pret).
