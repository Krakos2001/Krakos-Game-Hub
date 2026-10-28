
import json
from pathlib import Path

def load_records():
    log_path = Path(__file__).parent / "games" /  "logs" / "game_logs.jsonl"
    record = []
    try:
        with  open(log_path, "r", encoding="utf-8") as f:
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

def filter_records(records, filters, filter_category):
    matches = [record for record in records if record.get(filter_category) == filters]
    return matches

def compute_stat(records, game=None):
    game_played = len(records)
    
    won = len(filter_records(records, "won", "result"))

    won_records = filter_records(records, "won", "result")  

    lost = len(filter_records(records, "lost", "result"))

    abandoned = len(filter_records(records, "abandoned", "result"))

    if won + lost == 0:
        win_rate = None
    else:
        win_rate = won / (won + lost)

    if game_played == 0:
        abandon_rate = None
    else:
        abandon_rate = abandoned / game_played
    
    if won == 0:
        avg_attempts_per_win = None
    else:
        avg_attempts_per_win = sum(len(record["details"]["guesses"]) for record in won_records) / won

    if won == 0:
        fastest_win = None
        fastest_win_time = None
    else:
        fastest_win = min(won_records, key=lambda record: record["duration"])
        fastest_win_time = fastest_win["duration"]

    return {"games_played": game_played, "won": won, "lost": lost, "abandoned": abandoned, "win_rate": win_rate, "abandon_rate": abandon_rate, "avg_attempts_per_win": avg_attempts_per_win, "fastest_win": fastest_win, "fastest_win_time": fastest_win_time}

def show_stats():
    pass
