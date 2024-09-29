#!/usr/local/bin/python3
#coding: utf-8
# Licence: GNU AGPLv3

"""Links files defined here to various points in the system"""

from __future__ import annotations

import filecmp
import json
import logging
import logging.handlers
import os
import sys
import time

from dataclasses import dataclass
from datetime import datetime
from collections import deque
from pathlib import Path
from typing import Optional, List, Union, Tuple

#############
# Constants #
#############

LOG_PATH=f"{__file__}.log"

# Absolute path this script is in
SCRIPTPATH=Path(__file__).resolve(strict=True).parent
SUBLIME_PATH=Path("~/Library/Application Support/Sublime Text/Packages/User/").expanduser().resolve(strict=True)

########
# Logs #
########

log = logging.getLogger(f"{__name__}.log")
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

#############
# functions #
#############

def link(from_script_dir: str, to: str):
	from_path = (SCRIPTPATH / Path(from_script_dir)).resolve(strict=True)
	to_path = Path(to).expanduser().resolve()
	log.info(f"Linking {from_path} to {to_path}")
	if to_path.is_file() and filecmp.cmp(from_path, to_path):
		log.info("Files identicals")
	else:
		log.info("Files changed")
		if to_path.exists():
			to_path.unlink()
		to_path.symlink_to(from_path)

def main():
    link("gitconfig", "~/.gitconfig")
    link("gitignore_global", "~/.gitignore_global")
    link("Sublime/Preferences.sublime-settings", SUBLIME_PATH / "Preferences.sublime-settings")
    link("Sublime/py-template.sublime-snippet", SUBLIME_PATH / "py-template.sublime-snippet")
    link("Sublime/tmux-template.sublime-snippet", SUBLIME_PATH / "tmux-template.sublime-snippet")
    link(".tmux.conf", "~/.tmux.conf")


########
# Main #
########

if __name__ == "__main__":
    print('#'*80)
    main()