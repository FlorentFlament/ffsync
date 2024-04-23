ffsync stands for Flash Floppy sync.

ffsync synchronizes roms specified in a yaml configuration file with
the roms in a target directory.  The target directory would typically
be a USB key to be used in a [Gotek drive][1] flashed with
[FlashFloppy][2].

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
$ export FFSYNC_ROMS_DIR="<path-to-roms-directory>"
$ export FFSYNC_TARGET_DIR="<path-to-mounted-usb-key>"
$
$ ffsync --config-file dmlem-compilation.yaml
Using parameters:
config-file: dmlem-compilation.yaml
roms-path: <path-to-roms-directory>
dest-dir: <path-to-mounted-usb-key>

DSKA0000_dm_saved.st [skipping] Already there
DSKA0001_dungeon_master.st <- <path-to-roms-directory>/Dungeon Master (1987)(FTL)[cr Lord]/Dungeon Master (1987)(FTL)[cr Lord].st
DSKA0002_chaos_strikes_back_1.st <- <path-to-roms-directory>/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 1 of 2)(Game Disk)[cr Replicants]/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 1 of 2)(Game Disk)[cr Replicants].st
DSKA0003_chaos_strikes_back_2.st <- <path-to-roms-directory>/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 2 of 2)(Utility Disk)[cr Replicants]/Chaos Strikes Back v2.0 (1991)(FTL)(Disk 2 of 2)(Utility Disk)[cr Replicants].st
DSKA0004_lemmings.st <- <path-to-roms-directory>/Lemmings (1990)(Psygnosis)[cr BBC]/Lemmings (1990)(Psygnosis)[cr BBC].st
$
$ ls -l <path-to-mounted-usb-key>
total 3888
-rw-r--r-- 1 florent florent 737280 Apr 23 08:55 DSKA0000_dm_saved.st
-r--r--r-- 1 florent florent 737280 Apr 23 08:56 DSKA0001_dungeon_master.st
-r--r--r-- 1 florent florent 829440 Apr 23 08:56 DSKA0002_chaos_strikes_back_1.st
-r--r--r-- 1 florent florent 819200 Apr 23 08:56 DSKA0003_chaos_strikes_back_2.st
-r--r--r-- 1 florent florent 839680 Apr 23 08:56 DSKA0004_lemmings.st
-rw-r--r-- 1 florent florent  10241 Apr 17 00:00 FF.CFG
-rw-r--r-- 1 florent florent      1 Jan  1  2019 IMAGE_A.CFG
```

[1]: https://www.gotekemulator.com/
[2]: https://github.com/keirf/flashfloppy
