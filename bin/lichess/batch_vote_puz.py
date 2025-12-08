#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "diskcache",
#     "python-dotenv",
#     "requests",
# ]
# ///
import csv
import json
import os
import time

import requests

from typing import List, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv
from diskcache import Cache

load_dotenv()

TOKEN = os.getenv("LICHESS_PUZ_TAG_TOKEN")
CACHE = Cache("cache")

HEADERS = {
        "Authorization": f"Bearer {TOKEN}"
    }

THEMES = ["kingsideAttack", "queensideAttack", "long", "short"]

@dataclass(frozen=True)
class Puzzle:
    puzzle_id: str
    tags: List[str] = field(default_factory=list)
    remove_tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "puzzleId": self.puzzle_id,
            "themes": [{"theme": tag, "vote": True} for tag in self.tags] + [{"theme": tag, "vote": None} for tag in self.remove_tags]
        }

    def is_unchanged(self, all_errors:  dict[str, list[Any]]) -> bool:
        if my_errors := all_errors.get(self.puzzle_id, None):
            for err in my_errors:
                if err.get("theme", "") in self.tags and err.get("msg", "") != "unchanged":
                    return False
            return True

    
    def new_from_errors(self, all_errors: dict[str, list[Any]]) -> Puzzle | None:
        unchanged_themes = set()
        if my_errors := all_errors.get(self.puzzle_id, None):
            for err in my_errors:
                if err.get("msg", "") == "unchanged":
                    unchanged_themes.add(err.get("theme", ""))
        current_and_errors = list(set(self.tags).union(unchanged_themes))
        if unchanged_themes:
            return self.__class__(puzzle_id=self.puzzle_id, tags=unchanged_themes, remove_tags=self.remove_tags)



# input
# [
#     {
#       "puzzleId": "00SsI",
#       "errors": {
#         "theme": "pin",
#         "msg": "unchanged"
#       }
#     }
#   ]
def group_by_puzzle_id(errors: list[dict[str, Any]]) -> dict[str, list[Any]]:
    res = {}
    for puz_theme_error in errors:
        puz_id = puz_theme_error["puzzleId"]
        if puz_id not in res:
            res[puz_id] = []
        res[puz_id].append(puz_theme_error["errors"])
    return res

@CACHE.memoize()
def batch_vote(puzs: List[Puzzle]) -> dict[str, list[Any]] | None:
    # /api/puzzle/vote-themes
    url = "https://lichess.org/api/puzzle/vote-themes"
    data = {
        "votes": [puz.to_dict() for puz in puzs]
    }
    response = requests.post(url, headers=HEADERS, json=data)
    print("Response:", response.status_code)
    print("Body:", response.text)

    dumped = response.json()
    print("json", json.dumps(dumped, indent=2))
    if response.status_code == 400:
        return group_by_puzzle_id(dumped["error"])

def trigger_dirty(puzs: List[Puzzle]) -> None:
    dirty_req = []
    for puz in puzs:
        bogus_themes = [t for t in THEMES if t not in puz.tags]
        new_t = next(iter(bogus_themes))
        assert new_t is not None, f"need a new tag to make dirty, puz {puz}"
        dirty_req.extend([Puzzle(puzzle_id=puz.puzzle_id, tags=[new_t]), Puzzle(puzzle_id=puz.puzzle_id, remove_tags=[new_t])])
    if (errors := batch_vote(dirty_req)) is not None:
        unchanged = [puz.new_from_errors(errors or {}) for puz in puzs if puz.new_from_errors(errors or {})]
        if unchanged:
            trigger_dirty(unchanged)

def div_by_2_if_even_odd_plus_1(n: int) -> int:
    if n % 2 == 0:
        return n // 2
    return n // 2 + 1

def main():
    puzzles = []
    #trigger_dirty([Puzzle(puzzle_id="00QkV", tags=[])])
    with open("puzzle_new_tags.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            puzzle_id = row["PuzzleId"]
            tags = row["NewTags"].split()
            puzzles.append(Puzzle(puzzle_id, tags))

    batch_size = 500
    sleep_t = .3
    for i in range(8000, len(puzzles), batch_size):
        batch = puzzles[i:i+batch_size]
        print(f"Voting batch {i//batch_size + 1}: {len(batch)} puzzles")
        errors = batch_vote(batch)
        print("errors grouped", errors)

        unchanged = [puz for puz in batch if puz.is_unchanged(errors or {})]
        changed = [puz for puz in batch if not puz.is_unchanged(errors or {})]
        print("unchanged", len(unchanged))
        if changed:
            print("MODIFIED", changed)
        sub_batch_size = div_by_2_if_even_odd_plus_1(batch_size)
        for j in range(0,len(unchanged), sub_batch_size):
            sub_batch = unchanged[j:j+sub_batch_size]
            print(f"Re-voting unchanged sub-batch {j}: {len(sub_batch)} puzzles to trigger dirty")
            trigger_dirty(sub_batch)
            time.sleep(sleep_t)

        time.sleep(sleep_t)

    #batch_vote([Puzzle(puzzle_id="00SsI",remove_tags=["pin"])])

#db.puzzle2_round.find({ _id:'lichess:00QkV' })


# db.puzzle2_round.find({ _id: {$regex: '00QkV' }})

# db.puzzle2_puzzle.find({_id: '0oE25'})
# [
#   {
#     _id: '0oE25',
#     gameId: 'khz4OCAz',
#     fen: 'r4rk1/ppq1bppp/2p1b3/4P3/2P1Q3/6P1/PP3PK1/RNB4R b - - 4 17',
#     themes: [ 'middlegame', 'checkFirst' ],
#     glicko: {
#       r: 646.3184607755162,
#       d: 84.2956475070283,
#       v: 0.08999806956797396
#     },
#     plays: 42,
#     vote: 0.5714285969734192,
#     vu: 11,
#     vd: 3,
#     line: 'a8d8 e4h7',
#     cp: 999999999,
#     opening: [ 'Russian_Game', 'Russian_Game_Italian_Variation' ],
#     users: [ 'howiroll', 'vadimdu' ]
#   }
# ]
# puzzles [direct: primary] puzzler> db.puzzle2_round.find({ _id: 'lichess:0oE25'})
# [
#   {
#     _id: 'lichess:0oE25',
#     d: ISODate('2024-05-23T09:50:07.782Z'),
#     e: 100,
#     p: '0oE25',
#     t: [ '+mateIn1', '+mate', '+kingsideAttack', '+oneMove', '-zugzwang' ]
#   }
# ]














if __name__ == "__main__":
    print("#"*80)
    main()
