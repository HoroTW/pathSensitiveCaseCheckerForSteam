#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This Script is used to find issuse with save games of steam games.
It is not optimized or something - it is just a quick and dirty way that is good
enough to find the issue and show if it is solved. You could also use ext4
filesystems with case insensitivity enabled but I don't want that...
"""

import os
import argparse
from pathlib import Path as plPath
import re

globalFolderCounter, globalFileCounter = 0, 0
issueList = []


def main():
    parser = argparse.ArgumentParser(
        description=(
            f"Find folders with the same name but different case and reports "
            f"them, also showing if there is a symlink (indicating that the "
            f"issue might be fixed). Since this script is meant to be used on "
            f"Steam games it skips the wine drive 'z:'. If no path is given "
            f"it will try to find the steam library folders and search them."
        )
    )
    parser.add_argument(
        "path",
        metavar="path",
        type=str,
        nargs="*",
        help="path to search for folders with the same name but different case",
    )
    args = parser.parse_args()

    if args.path:
        path = args.path[0]
        assert os.path.exists(path), "Path does not exist: " + path
        findFoldersWithSameNameButDifferentCase(path)
    else:
        print("No path given - checking for steam library folders")
        folders = autofindLibraryFolders()
        
        print("")
        for folder in folders:
            print(f"starting search in {folder}")
            if not os.path.exists(folder):
                print(f"Stem library folder {folder} does not exist - skipping")
                continue
            findFoldersWithSameNameButDifferentCase(folder)
    printResults()


def autofindLibraryFolders():
    steamdirs = (
        "~/.local/share/Steam/config/libraryfolders.vdf",  # native
        "~/.var/app/com.valvesoftware.Steam/.local/share/Steam/config/libraryfolders.vdf",  # flatpak
    )
    paths = []

    for steamdir in steamdirs:
        print(f"checking for {steamdir}")

        if os.path.exists(os.path.expanduser(steamdir)):
            with open(os.path.expanduser(steamdir), "r", encoding="utf-8") as f:
                content = f.read()
                # rg filter to get the paths
                tmp = [
                    m.group(1)
                    for m in re.finditer(r'"path"\W+"(.+)"$', content, re.MULTILINE)
                ]
                paths.extend(tmp)
    print("")

    # remove duplicates
    paths = list(dict.fromkeys(paths))
    for path in paths:
        print(f"found: {path}")

    return paths


def findFoldersWithSameNameButDifferentCase(path):
    """
    Find folders with the same name but different case - recursive
    """
    global globalFolderCounter, globalFileCounter, issueList

    if os.path.islink(path):
        if plPath(path).parts[-1] == "z:":  # skip wine drive
            return

    globalFolderCounter += 1

    # Get all folders in current path
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    # Get all folders with the same name but different case
    for folder in folders:
        for otherFolder in folders:
            if folder.lower() == otherFolder.lower() and folder != otherFolder:
                # issue found append both folders to issueList
                f1 = os.path.join(path, folder)
                f2 = os.path.join(path, otherFolder)
                alternativeForm = (f2, f1)
                if alternativeForm not in issueList:
                    issueList.append((f1, f2))

        # Recursion
        findFoldersWithSameNameButDifferentCase(os.path.join(path, folder))

    # also check files
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # get all files with the same name but different case
    for file in files:
        globalFileCounter += 1
        for otherFile in files:
            if file.lower() == otherFile.lower() and file != otherFile:
                # issue found append both files to issueList
                f1 = os.path.join(path, file)
                f2 = os.path.join(path, otherFile)
                alternativeForm = (f2, f1)
                if alternativeForm not in issueList:
                    issueList.append((f1, f2))


def printResults():
    """
    Print the results
    """
    global globalFolderCounter, globalFileCounter, issueList

    print("\nFolders checked: " + str(globalFolderCounter))
    print("Files checked: " + str(globalFileCounter))
    print("Issues found: " + str(len(issueList)))
    for issue in issueList:
        pathWithoutFolder = os.path.join(*plPath(issue[0]).parts[:-1])
        folderVariant1 = plPath(issue[0]).parts[-1]
        folderVariant2 = plPath(issue[1]).parts[-1]

        print(f"  - {pathWithoutFolder}/{'.' * len(folderVariant1)}")
        print(f"{' ' * len(pathWithoutFolder)}V1: /{folderVariant1}", end=" ")

        # check if folder1 is a symlink to folder2
        if os.path.islink(issue[0]):
            linkTarget = plPath(issue[0]).resolve()

            if linkTarget == plPath(issue[1]):
                print(f"-> {folderVariant2}")
                continue
        print("")

        print(f"{' ' * len(pathWithoutFolder)}V2: /{folderVariant2}", end=" ")
        # check if folder2 is a symlink to folder1
        if os.path.islink(issue[1]):
            linkTarget = plPath(issue[1]).resolve()

            if linkTarget == plPath(issue[0]):
                print(f"-> {folderVariant1}")
                continue
        print("")


if __name__ == "__main__":
    main()
