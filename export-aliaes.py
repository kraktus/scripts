#!/usr/local/bin/python3
#coding: utf-8
# Licence: GNU AGPLv3

""""""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import sys

from argparse import RawTextHelpFormatter
from dataclasses import dataclass
from datetime import datetime
from collections import deque
from pathlib import Path
from typing import Optional, List, Union, Tuple

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
log.addHandler(handler_2)

###########
# Classes #
###########

def main() -> None:
	# concatenate all the files in zsh/*.zsh folder as exported-aliases.sh
	res = []
	for file in Path("zsh").glob("*.zsh"):
		with open(file, "r") as f:
			# strip comments
			lines = [line for line in f.readlines() if not (line.startswith("#") or line.strip() == "")]
			res.extend(lines)
	with open("exported-aliases.sh", "w") as f:
		f.write("\n".join(res))
########
# Main #
########

if __name__ == "__main__":
    print('#'*80)
    main()