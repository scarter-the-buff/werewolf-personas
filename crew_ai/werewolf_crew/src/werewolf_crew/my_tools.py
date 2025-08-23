# src/werewolf_crew/my_tools.py
from typing import List, Dict
import json
import os

VOTES_PATH = "./memories/votes.jsonl"

def _append_jsonl(path: str, obj: Dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _read_jsonl(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

# --- public helpers your Python orchestration calls ---

def write_votes(phase: str, votes: List[Dict]):
    """
    votes: list like [{"voter":"Player 1","vote":"Player 5"}, ...]
    """
    for v in votes:
        _append_jsonl(VOTES_PATH, {"phase": phase, **v})

def read_votes(phase: str) -> List[Dict]:
    return [o for o in _read_jsonl(VOTES_PATH) if o.get("phase") == phase]

def clear_votes(phase: str) -> None:
    data = _read_jsonl(VOTES_PATH)
    remaining = [o for o in data if o.get("phase") != phase]
    with open(VOTES_PATH, "w", encoding="utf-8") as f:
        for o in remaining:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

# Backwards-compat function names if your other code refers to them
def clear_votes_func(phase: str) -> str:
    clear_votes(phase)
    return "OK"

def dead_votes_func(phase: str) -> str:
    # Kept for compatibility with your previous import; returns JSON string
    try:
        return json.dumps(read_votes(phase), ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
