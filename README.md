# Gen 3 Physical/Special Split

Patches that give the Game Boy Advance Pokémon games the **Gen 4 physical/special split**.
Each move is Physical, Special or Status based on the move itself, not its type, using its
Diamond/Pearl/Platinum category. The games also show each move's category in-game: on the
summary screen, when learning a move, at the Move Relearner/Tutor, and in the TM Case or
Bag. The trainer AI is updated to reason about the categories too.

> **Pokémon Colosseum / XD: Gale of Darkness:** these GameCube games aren't covered here.
> [GoD Tool](https://projectpokemon.org/home/files/file/2463-gale-of-darkness-tool-osx-colosseum-tool/) (and its Colosseum Tool) has a
> patch that applies the Gen 4 physical/special split to both.

| FireRed / LeafGreen | Ruby / Sapphire | Emerald |
|---|---|---|
| ![](FireRed-LeafGreen/screenshots/summary_shadow_ball_special.png) | ![](Ruby-Sapphire/screenshots/summary_shadow_ball_special.png) | ![](Emerald/screenshots/summary_shadow_ball_special.png) |
| ![](FireRed-LeafGreen/screenshots/tm_case_earthquake_physical.png) | ![](Ruby-Sapphire/screenshots/bag_tm_earthquake_physical.png) | ![](Emerald/screenshots/bag_tm_earthquake_physical.png) |

Each game's README has screenshots of every changed screen.

## Supported ROMs

Find your ROM, then use that patch. Each game's README has the SHA-1s and game-specific
notes.

| Your ROM (clean, English) | Patch | ROM CRC32 |
|---|---|---|
| FireRed (USA) v1.0 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md)`FireRed_PhysSpecSplit_v1.0.bps` | `DD88761C` |
| FireRed (USA) v1.1 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md)`FireRed_PhysSpecSplit_v1.1.bps` | `84EE4776` |
| LeafGreen (USA) v1.0 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md)`LeafGreen_PhysSpecSplit_v1.0.bps` | `D69C96CC` |
| LeafGreen (USA) v1.1 | [`FireRed-LeafGreen/`](FireRed-LeafGreen/README.md)`LeafGreen_PhysSpecSplit_v1.1.bps` | `DAFFECEC` |
| Ruby (USA, Europe) v1.0 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Ruby_PhysSpecSplit_v1.0.bps` | `F0815EE7` |
| Ruby (USA, Europe) Rev 1 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Ruby_PhysSpecSplit_v1.1.bps` | `61641576` |
| Ruby (USA, Europe) Rev 2 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Ruby_PhysSpecSplit_v1.2.bps` | `AEAC73E6` |
| Sapphire (USA, Europe) v1.0 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Sapphire_PhysSpecSplit_v1.0.bps` | `554DEDC4` |
| Sapphire (USA, Europe) Rev 1 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Sapphire_PhysSpecSplit_v1.1.bps` | `BAFEDAE5` |
| Sapphire (USA, Europe) Rev 2 | [`Ruby-Sapphire/`](Ruby-Sapphire/README.md)`Sapphire_PhysSpecSplit_v1.2.bps` | `9CC4410E` |
| Emerald (USA, Europe) | [`Emerald/`](Emerald/README.md)`Emerald_PhysSpecSplit.bps` | `1F1C08FB` |

* The ROM must be a **clean, unmodified** dump of that exact version. Other languages and
  already-hacked ROMs aren't supported.
* Not sure which revision you have? BPS patches check the original ROM's checksum, so a
  patcher refuses the wrong one: try each patch for your game in turn. You can also
  compare your ROM's CRC32 (Rom Patcher JS shows it) or SHA-1 (`shasum rom.gba`).
* The patches don't change the save format, so **existing saves keep working**. Back up
  your `.sav` first anyway.

## How to apply a patch

**You need your own ROM.** A `.bps` patch isn't a game: it only lists the differences from
the original ROM. A patcher reads your clean ROM and the patch, and writes a new, patched
`.gba` for you to play. Your original ROM is left unchanged. The patch checks the ROM's
checksum first, so it refuses the wrong game or revision. Building from source (below)
compiles a complete ROM, but it still needs your clean ROM, both to confirm which game
and revision you're building and to make the `.bps` from.

Any BPS patcher works. For example:

**Rom Patcher JS (browser, any OS):**
1. Open <https://www.marcrobledo.com/RomPatcher.js/>.
2. *ROM file*: choose your clean `.gba`.
3. *Patch file*: choose the matching `.bps`.
4. Click **Apply patch** and save the new `.gba`.

**Floating IPS (Flips), Windows/Linux:** click **Apply Patch**, select the `.bps`, then your
clean ROM, then where to save the patched ROM.

**mGBA soft-patching (no new file is written):** put the `.bps` next to the ROM with the
same file name (e.g. `Pokemon Emerald.gba` + `Pokemon Emerald.bps`) and mGBA applies it on
load. Or from a terminal: `mGBA -p Emerald_PhysSpecSplit.bps "Pokemon Emerald.gba"`.

**Command line (Python 3, no dependencies):**
```sh
python3 tools/bps.py apply "Pokemon Emerald.gba" Emerald/Emerald_PhysSpecSplit.bps "Emerald Split.gba"
```

Then play the patched `.gba` in any GBA emulator or on a flash cart.

## What changed in battle

The same in every game:

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

### Why it matters

In the original games, a move's type decided which stat it used: Normal, Fighting, Flying,
Poison, Ground, Rock, Bug, Ghost and Steel moves were physical; Fire, Water, Grass,
Electric, Psychic, Ice, Dragon and Dark moves were special. Many Pokémon ended up with their
own type's moves running off their weaker attacking stat:

<details>
<summary>Show Pokémon that gain</summary>

| Pokémon (base Attack / Sp. Atk) | Move | Original games | With this patch |
|---|---|---|---|
| **Kingler** (130 / 50), **Crawdaunt** (120 / 90) | Crabhammer | Special: their signature move used their weaker Sp. Atk (Kingler's is just 50) | Physical: uses their 130 / 120 Attack |
| **Sneasel** (95 / 35) | Faint Attack | Special: its Dark STAB used one of the lowest Sp. Atk stats in the game | Physical: uses its 95 Attack |
| **Gyarados** (125 / 60) | Waterfall | Special: its Water STAB used its weak Sp. Atk, so it usually ran Normal and Ground moves instead | Physical: uses its 125 Attack |
| **Gengar** (65 / 130) | Shadow Ball, Sludge Bomb | Physical: its own STAB moves used its weak Attack, so Gengar was usually given Psychic or Thunderbolt instead | Special: uses its 130 Sp. Atk |
| **Omastar** (60 / 115) | Ancient Power | Physical: its Rock STAB used its 60 Attack | Special: uses its 115 Sp. Atk |
| **Absol** (130 / 75) | Bite | Special: its Dark STAB used its weaker Sp. Atk | Physical: uses its 130 Attack |
| **Hitmonchan** (105 / 35) | Fire / Ice / Thunder Punch | Special: its signature punches used its 35 Sp. Atk | Physical: uses its 105 Attack |

</details>

It goes both ways. Some Pokémon lose out, exactly as they did in Gen 4:

<details>
<summary>Show Pokémon that lose out</summary>

| Pokémon (base Attack / Sp. Atk) | Move | Original games | With this patch |
|---|---|---|---|
| **Shedinja** (90 / 30) | Shadow Ball | Physical: its Ghost STAB used its 90 Attack | Special: uses its 30 Sp. Atk |
| **Jynx** (50 / 115) | Ice Punch | Special: its Ice STAB used its 115 Sp. Atk | Physical: uses its 50 Attack |
| **Dodrio** (110 / 60) | Tri Attack | Physical: its Normal STAB used its 110 Attack | Special: uses its 60 Sp. Atk |
| **Snorlax** (110 / 65), **Slaking** (160 / 95), **Ursaring** (130 / 75) | Hyper Beam | Physical: their Normal STAB finisher used their Attack | Special: uses their Sp. Atk, about 0.6× their Attack |
| **Muk** (105 / 65) | Sludge Bomb, Sludge | Physical: its Poison STAB used its 105 Attack | Special: uses its 65 Sp. Atk |
| **Latios** (90 / 130) | Dragon Claw | Special: its Dragon STAB used its 130 Sp. Atk | Physical: uses its 90 Attack |

</details>

### Trainer AI

The AI decides whether some moves are worth using by guessing whether your Pokémon
attacks physically or specially. The original games guessed from **your Pokémon's types**
(using the same type-based lists as above), or from the **type of the move you last used**.
The patch changes these guesses to:

* **Your Pokémon's last move:** its actual category. Used for Counter, Mirror Coat, and
  Defense / Sp. Def boosts (e.g. Harden or Amnesia after you hit it).
* **Your Pokémon itself:** whichever of its Attack and Sp. Atk is higher (a tie counts as
  both). Used for Reflect, Light Screen, Attack / Sp. Atk drops (Growl, etc.), and Counter /
  Mirror Coat before you've attacked.

Measured with the [AI test](docs/DEVELOPING.md#ai-test) (average change to the move's score over 256 runs;
the AI usually picks its highest-scoring move, so a drop of 1–2 points makes a move much
less likely). FireRed shown; the other games differ by at most 0.15:

| Situation | AI's move | Before | After |
|---|---|---|---|
| vs a Gengar-like Pokémon (Ghost/Poison, Sp. Atk > Attack) | Reflect | +0.00 | −1.54 |
| | Light Screen | −1.61 | +0.00 |
| vs a Gyarados-like Pokémon (Water/Flying, Attack > Sp. Atk) | Light Screen | +0.00 | −1.55 |
| | Growl | −1.52 | +0.00 |
| after you used Shadow Ball (now special) | Counter | +0.59 | −1.00 |
| after you used Crunch (now physical) | Mirror Coat | +0.61 | −1.00 |
| after you used Crunch (now physical) | Counter | −1.00 | +0.63 |
| after you used Shadow Ball (now special) | Mirror Coat | −1.00 | +0.64 |

So the AI now puts up Light Screen, not Reflect, against Gengar. It stops using Counter
on a special Shadow Ball (which Counter can't reflect) and Mirror Coat on a physical Crunch,
and does the opposite where the old AI was wrong the other way: it now favours Counter
after a physical Crunch and Mirror Coat after a special Shadow Ball.

### Known limitations

* The category isn't shown in the battle move menu. Check it from the party summary
  screen, or the TM Case / Bag for TMs.
* The AI's guess about your Pokémon compares its Attack and Sp. Atk; it doesn't look at
  which moves it actually knows.

## Building from source

The patches are built from [pret](https://github.com/pret)'s decompilations of the games.
Each game folder holds its source changes as `source/phys-spec-split.diff`, and `tools/`
has scripts to set up a working copy, rebuild the patches and run the tests. See
[docs/DEVELOPING.md](docs/DEVELOPING.md) for how to change a patch, build it with or
without the scripts, and how the screenshots and AI numbers were produced.

## Credits and license

* The [pret](https://github.com/pret) decompilations and agbcc compiler.
* Move categories are from Generation 4, checked against [Pokémon Showdown's move data](https://play.pokemonshowdown.com/data/moves.json)
  ([source](https://github.com/smogon/pokemon-showdown/blob/master/data/moves.ts)).

The patches, scripts and source changes in this repository are released under the
[MIT License](LICENSE). This repository contains no ROMs or game data: you need your own
clean ROM. Pokémon is © Nintendo, Creatures Inc. and GAME FREAK inc.; this project is not
affiliated with or endorsed by them.
