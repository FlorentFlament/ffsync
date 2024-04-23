Tool I use to manage (Atari ST) roms on a USB key to be used on my
Gotek / Flash Floppy drive.

# Usage

ffsync synchronizes roms specified in a yaml configuration file with
the roms in a target directory.  The target directory would typically
be a USB key to be used in a Gotek drive flashed with flash floppy.

```
$ cat dmlem-compilation.yaml
---
dm-saved:
    0: dm-saved-games.st
dungeon-master:
    1: Dungeon Master (1987)(FTL)[cr Lord].st
chaos-strikes-back:
    2: Chaos Strikes Back v2.0 (1991)(FTL)(Disk 1 of 2)(Game Disk)[cr Replicants].st
    3: Chaos Strikes Back v2.0 (1991)(FTL)(Disk 2 of 2)(Utility Disk)[cr Replicants].st
lemmings:
    4: Lemmings (1990)(Psygnosis)[cr BBC].st
$
$ export TOSYNC_ROMS_PATH="$<path-to>/tosec-atari-st-games/"
$ export TOSYNC_DEST_DIR="<path-to-mounted-usb-key>/"
$
$ ffsync --config-file dmlem-compilation.yaml
Using parameters:
config-file: dmlem-compilation.yaml
roms-path: <path-to>/tosec-atari-st-games/
dest-dir: <path-to-mounted-usb-key>

DSKA0000_dm_saved.st [skipping] Already there
DSKA0001_dungeon_master.st <- <path-to>/tosec-atari-st-games/Dungeon Master (1987)(FTL)[cr Lord]/Dungeon Master (1987)(FTL)[cr Lord].st
DSKA0002_chaos_strikes_back_1.st <- <path-to>/tosec-atari-st-games/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 1 of 2)(Game Disk)[cr Replicants]/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 1 of 2)(Game Disk)[cr Replicants].st
DSKA0003_chaos_strikes_back_2.st <- <path-to>/tosec-atari-st-games/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 2 of 2)(Utility Disk)[cr Replicants]/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 2 of 2)(Utility Disk)[cr Replicants].st
DSKA0004_lemmings.st <- <path-to>/tosec-atari-st-games/Lemmings (1990)(Psygnosis)[cr BBC]/Lemmings (1990)(Psygnosis)[cr BBC].st
```
