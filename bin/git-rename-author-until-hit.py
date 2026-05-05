#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.8"
# dependencies = [
# ]
# ///
#
# coding: utf-8
# Licence: GNU AGPLv3

""""""
import subprocess
import sys
import tempfile
import os

TARGET_NAME = "kraktus"
TARGET_EMAIL = "kraktus@users.noreply.github.com"

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def get_commits():
    return run(["git", "rev-list", "HEAD"]).splitlines()


def get_author(commit):
    name = run(["git", "show", "-s", "--format=%an", commit])
    email = run(["git", "show", "-s", "--format=%ae", commit])
    return name, email


def find_stop_commit():
    # wait to find a first bad commit
    dirty = 0
    for commit in get_commits():
        name, email = get_author(commit)
        if (dirty >= 2) and name == TARGET_NAME and email == TARGET_EMAIL:
            return commit
        else:
            dirty += 1
    return None


def main():
    stop_commit = find_stop_commit()

    if not stop_commit:
        print(f"No commit found with author {TARGET_NAME} <{TARGET_EMAIL}>")
        sys.exit(1)

    print(f"Stopping at commit: {stop_commit}")
    if not input('Continue? '):
        print("Stopping")
        sys.exit(0)

    # Prepare rebase todo editor script
    editor_script = tempfile.NamedTemporaryFile(delete=False, mode="w")
    editor_script.write("""#!/bin/bash
sed -i '' 's/^pick /edit /g' "$1"
""")
    editor_script.close()
    os.chmod(editor_script.name, 0o755)

    env = os.environ.copy()
    env["GIT_SEQUENCE_EDITOR"] = editor_script.name

    # Start interactive rebase
    subprocess.run(["git", "rebase", "-i", stop_commit], env=env)

    # Now amend each commit automatically
    while True:
        try:
            subprocess.run([
                "git", "commit", "--amend",
                f"--author={TARGET_NAME} <{TARGET_EMAIL}>",
                "--no-edit"
            ], check=True)

            subprocess.run(["git", "rebase", "--continue"], check=True)

        except subprocess.CalledProcessError:
            break

    print("Done rewriting commits.")


if __name__ == "__main__":
    main()