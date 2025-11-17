#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
#     "requests",
# ]
# ///
#
# coding: utf-8
# Licence: GNU AGPLv3

""""""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import subprocess
import sys

from argparse import RawTextHelpFormatter
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, List, Union, Tuple


#############
# Constants #
#############

LOG_PATH = f"{__file__}.log"

########
# Logs #
########

log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)
format_string = "%(asctime)s | %(levelname)-8s | %(message)s"

# 125000000 bytes = 12.5Mb
handler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=12500000, backupCount=3, encoding="utf8")
handler.setFormatter(logging.Formatter(format_string))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

handler_2 = logging.StreamHandler(sys.stdout)
handler_2.setFormatter(logging.Formatter(format_string))
handler_2.setLevel(logging.INFO)
if __debug__:
    handler_2.setLevel(logging.DEBUG)
log.addHandler(handler_2)

###########
# Classes #
###########

# recusrively find git dirs, check if remote named `remote_from` exists, and ask user if they want to change it to `remote_to`
def recursive_git_remote_change(dir_: Path, *, remote_from: str, remote_to: str) -> None:
    """
    Recursively search for .git directories under `dir_`, check if remote named `remote_from` exists,
    and prompt user to change it to `remote_to` in each repo found.
    """
    for git_dir in dir_.rglob('.git'):
        repo_path = git_dir.parent
        try:
            # Get the list of remotes
            remotes = subprocess.check_output(
                ["git", "remote", "-v"], cwd=repo_path, text=True
            ).splitlines()
        except subprocess.CalledProcessError:
            print(f"Failed to list remotes in {repo_path}")
            continue

        filtered = [remote for remote in remotes if (remote_from in remote)]
        if len(filtered) > 0:
            print(f"Found remote '{remote_from}' in repo: {repo_path}")
            print(filtered[0])
            #assert (not "kraktus" in filtered[0])
            answer = input(f"Change to '{remote_to}'? [y/N]: ").strip().lower()
            if answer == 'y':
                try:
                    subprocess.check_call(
                        ["git", "remote", "rename", remote_from, remote_to], cwd=repo_path
                    )
                    print(f"Renamed remote '{remote_from}' to '{remote_to}' in {repo_path}")
                except subprocess.CalledProcessError:
                    print(f"Failed to rename remote in {repo_path}")
            else:
                print(f"Skipped renaming in {repo_path}")



def doc(dic: Dict[str, Callable[..., Any]]) -> str:
    """Produce documentation for every command based on doc of each function"""
    doc_string = ""
    for name_cmd, func in dic.items():
        doc_string += f"{name_cmd}: {func.__doc__}\n\n"
    return doc_string

def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    # commands = {
    # "cmd": cmd_function,
    # }
    # parser.add_argument("command", choices=commands.keys(), help=doc(commands))
    parser.add_argument(
        "dir",
        help="Directory containing where to look for git repos",
        type=Path,
    )
    parser.add_argument(
        "--remote_from",
        "-f",
        help="Directory containing where to look for git repos",
        type=str,
    )
    parser.add_argument(
        "--to",
        "-t",
        help="Directory containing where to look for git repos",
        type=str,
    )

    args = parser.parse_args()
    recursive_git_remote_change(args.dir, remote_from=args.remote_from, remote_to=args.to)

########
# Main #
########

if __name__ == "__main__":
    print('#'*80)
    main()