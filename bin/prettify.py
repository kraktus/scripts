#!/usr/local/bin/python3
#coding: utf-8
# Licence: GNU AGPLv3

"""Prettify JSON or printed python dict"""

from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import sys
import traceback
import re

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
if __debug__:
    handler_2.setLevel(logging.DEBUG)
log.addHandler(handler_2)

###########
# Classes #
###########

def to_double_quotes(s: str) -> str:
    return s.replace("'", '"')

def to_json_bool(s: str) -> str:
    return s.replace("True", "true").replace("False", "false")

# transforms datetime.datetime(2024, 12, 5, 14, 6, 10, tzinfo=tzutc()) to "2024-12-05T14:06:10"
def to_iso_date(s: str) -> str:
    # with regex
    return re.sub(r"datetime\.datetime\((\d{4}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), (\d{1,2}), tzinfo=tzutc\(\)\)", r'"\1-\2-\3T\4:\5:\6"', s)

def identity(s: str) -> str:
    return s

transfos = [identity, to_double_quotes, to_json_bool, to_iso_date]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=Path, help="Path to the JSON file")
    # first try to read as json
    args = parser.parse_args()
    json_txt = args.json_file.read_text()
    json_dict = None
    for transfo in transfos:
        print(f"trying with transformation {transfo.__name__}")
        json_txt = transfo(json_txt)
        try:
            json_dict = json.loads(json_txt)
        except json.JSONDecodeError as e:
            # using traceback to print the error
            print(f"Could not decode as JSON, error was {e}")
            traceback.print_exc()
    print("json_txt", json_txt)
    if json_dict == None:
        print("trying as python dict")
        print("Warning: this may be a security risk")
        # input to proceed
        proceed = input("Proceed? [y/N]: ")
        if proceed.lower() != "y" or not proceed:
            sys.exit(1)
        with args.json_file.open() as f:
            # warning as input 
            json_dict = eval(f.read())

    # save as `pretty_filename.json`
    pretty_filename = args.json_file.with_suffix(".pretty.json")
    with pretty_filename.open("w") as f:
        json.dump(json_dict, f, indent=2)

########
# Main #
########

if __name__ == "__main__":
    print('#'*80)
    main()
    #print(to_iso_date("datetime.datetime(2024, 12, 5, 14, 6, 10, tzinfo=tzutc())"))
    #print(to_iso_date('"UsageOperationUpdateTime": datetime.datetime(2024, 12, 5, 14, 13, 51, tzinfo=tzutc()),'))


