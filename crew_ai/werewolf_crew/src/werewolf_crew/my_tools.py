from crewai.tools import tool
import json
import os

VOTES_PATH = "./memories/votes.jsonl"

def _append_jsonl(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _read_jsonl(path):
    if not os.path.exists(path): return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
    
@tool
def record_vote(phase: str, voter: str, vote: str) -> str:
    """
    Append a vote.

    Args:
        phase: "night" or "day"
        voter: name of the player casting the vote (e.g. "Player 1")
        vote:  name of the player voted against (e.g. "Player 5")

    Returns "OK" on success.
    """
    obj = {"phase": phase, "voter": voter, "vote": vote}
    _append_jsonl(VOTES_PATH, obj)
    return "OK"

@tool
def read_votes(phase: str) -> str:
    """
    Read back all votes for the given phase ("night" or "day") as JSON.
    """
    try:
        data = [o for o in _read_jsonl(VOTES_PATH) if o.get("phase")==phase]
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def clear_votes(phase: str) -> str:
    """
    Remove votes of a given phase from the store.
    """
    data = _read_jsonl(VOTES_PATH)
    remaining = [o for o in data if o.get("phase") != phase]
    with open(VOTES_PATH, "w", encoding="utf-8") as f:
        for o in remaining:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    return "OK"
