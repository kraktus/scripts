#!/usr/bin/python3
#coding: utf-8
# Licence: GNU AGPLv3

# nano ~/.local/bin/cron/cpu-monitoring.py

# crontab -e
# * * * * * ~/.local/bin/cron/cpu-monitoring.py

# alias rsi="echo 0 > ~/.local/bin/cron/cpu-usage.txt"
# alias idle="cat ~/.local/bin/cron/cpu-usage.txt"

"""Monitor CPU usage, and shut down if idle for more than 15 minutes"""


from __future__ import annotations

import argparse
import json
import logging
import logging.handlers
import os
import subprocess
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
FILE_NAME = os.path.basename(__file__)
LOCAL_HOME = str(Path.home())
PARENT_DIR = Path(__file__).resolve().parent
CPU_USAGE_LOG_FILE = f"{PARENT_DIR}/cpu-usage.txt"

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

def run(cmd: str, *args, **kwargs) -> subprocess.CompletedProcess:
    """Run a command while logging its input/output"""
    log.debug(f"running: {cmd.split()}")
    exc = subprocess.run(cmd.split(),*args, **kwargs)
    log.debug(f"exc {exc} stdout {exc.stdout} stderr {exc.stderr}")
    return exc

def run_capture(cmd: str) -> str:
    """Run a command and return the output"""
    return run(cmd,capture_output=True, text=True).stdout.strip()

def get_idle_time() -> int:
    """Get idle time in minutes"""
    if not os.path.exists(CPU_USAGE_LOG_FILE):
        return 0
    with open(CPU_USAGE_LOG_FILE) as f:
        return int(f.read())

def set_idle_time(idle_time: int) -> None:
    """Set idle time"""
    with open(CPU_USAGE_LOG_FILE, "w") as f:
        log.debug(f"setting idle_time to {idle_time}")
        f.write(str(idle_time))

def inc_idle_time() -> None:
    """Increment idle time"""
    log.debug("incrementing idle_time")
    idle_time = get_idle_time()
    set_idle_time(idle_time + 1)

def get_cpu_usage() -> float:
    """Get CPU usage"""
    cpus_usage = run_capture("ps aux").splitlines()[1:]
    # remove the line containing the program
    cpus_usage = filter(lambda x: FILE_NAME not in x, cpus_usage)
    return max([float(line.split()[2]) for line in cpus_usage])

def cpu_monitoring() -> None:
    """Monitor CPU usage"""
    cpu_usage = get_cpu_usage()
    log.info(f"cpu_usage: {cpu_usage}")
    if cpu_usage >= 5:
        set_idle_time(0)
    else:
        inc_idle_time()
    if get_idle_time() >= 15:
        set_idle_time(0)
        log.info("shutting down")
        try:
            run("sudo shutdown")
        except Exception as e:
            log.error(f"error shutting down with sudo: {e}")
            run("shutdown")


def main() -> None:
    cpu_monitoring()


########
# Main #
########

if __name__ == "__main__":
    print('#'*80)
    main()