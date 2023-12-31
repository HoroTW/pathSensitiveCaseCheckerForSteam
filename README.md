# Path Case Checker for Steam

This is just a little Python script that can be used to find issues with Steam games on case sensitive file systems.

I had a problem where my savegames would not load because the game was looking for a folder with a different case than the one it created. This typically happens when you switch from a case-insensitive/insane file system like NTFS to a case-sensitive file system like ext4/btrfs etc.

This is not optimised or anything - it is just a quick and dirty way that is good enough to find the issue (and show if it is probably fixed).

You could also use ext4 filesystems with case insensitivity enabled, but I don't want to...

## Requirements
Besides Python3 nothing is needed.


## Usage

```
> python3 pathCaseCheckerForSteam.py --help

usage: pathCaseCheckerForSteam.py [-h] [path ...]

Find folders with the same name but different case and reports them, also showing if there is a symlink (indicating that the issue might be fixed). Since this script is
meant to be used on Steam games it skips the wine drive 'z:'. If no path is given it will try to find the steam library folders and search them.

positional arguments:
path        path to search for folders with the same name but different case

options:
-h, --help  show this help message and exit
```

## Examples
```
> python3 pathCaseCheckerForSteam.py  # it will use the default steam path and 
                                      # flatpak path to search for you librarys

No path given - checking for steam library folders
checking for ~/.local/share/Steam/config/libraryfolders.vdf
checking for ~/.var/app/com.valvesoftware.Steam/.local/share/Steam/config/libraryfolders.vdf

found: /home/user/.local/share/Steam
found: /mnt/hdd1/SteamLibrary
found: /home/user/.var/app/com.valvesoftware.Steam/.local/share/Steam
found: /mnt/externaldrive/SteamLibrary

starting search in /home/user/.local/share/Steam
starting search in /mnt/hdd1/SteamLibrary
starting search in /home/user/.var/app/com.valvesoftware.Steam/.local/share/Steam
starting search in /mnt/externaldrive/SteamLibrary

Folders checked: 38472
Files checked: 387715
Issues found: 1
  - /mnt/hdd1/SteamLibrary/steamapps/common/Half-Life Alyx/game/hlvr/....
                                                                 V1: /SAVE 
                                                                 V2: /save -> SAVE
```

```
> python3 pathCaseCheckerForSteam.py /path/to/check # with explicit path

Folders checked: 14952
Files checked: 114923
Issues found: 1
  - /mnt/hdd1/SteamLibrary/steamapps/common/Half-Life Alyx/game/hlvr/....
                                                                 V1: /SAVE 
                                                                 V2: /save -> SAVE
```
