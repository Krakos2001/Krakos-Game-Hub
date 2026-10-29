import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

LOG_VERSION = 1
LOG_PATH = Path(__file__).parent / "games" / "logs" / "game_logs.jsonl"

def load_records():
    record = []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record.append(json.loads(line))
                except ValueError:
                    continue
    except FileNotFoundError:
        return record
    return record

def generate_unique_id():
    existing_records = load_records()
    existing_ids = {record["id"] for record in existing_records if "id" in record}
    while True:
        new_id = secrets.token_hex(3)

        if new_id not in existing_ids:
            return new_id

def save_stat(game, result, duration, details):
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    game_id = generate_unique_id()
    line = {"id": game_id, "v": LOG_VERSION, "date": date, "game": game, "result": result, "duration": duration, "details": details}
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")

def get_best_win_time(game):
    # fastest win of a game, None if the game was never won
    times = [record["duration"] for record in load_records()
             if record.get("game") == game and record.get("result") == "won"]
    return min(times, default=None)

def get_best_score(game):
    # best score of a game that has a score, 0 if there is none yet
    scores = [record["details"]["score"] for record in load_records()
              if record.get("game") == game and record.get("result") == "finished"]
    return max(scores, default=0)