import importlib
import pkgutil
import games
from pathlib import Path
from msvcrt import getwch
import json

AZERTY_ROW = ["&", "é", '"', "'", "(", "-", "è", "_", "ç", "à"]   # keys 1 to 9, then 0
WIDTH = 49
RESET = "\033[0m"
NORMAL = "\033[48;2;58;58;60m\033[1;97m"                 # dark gray, white bold text
HIGHLIGHT = "\033[48;2;200;200;200m\033[1m\033[38;2;30;30;30m"  # light gray, dark bold text


def load_games():
    loaded_games = []
    for item in pkgutil.iter_modules(games.__path__):
        loaded_games.append(importlib.import_module(f"games.{item.name}"))
    return loaded_games

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
        avg_attemps_per_win = sum(record["details"]["guesses"] for record in won_records) / won

    if won == 0:
        fastest_win = None
        fastest_win_time = None
    else:
        fastest_win = min(won_records, key=lambda record: record["duration"])
        fastest_win_time = fastest_win["duration"]
    


            

def print_row(text, color=NORMAL):
    print(f"{color}{text:<{WIDTH}}{RESET}")
    

def draw_menu(options, selected):
    title = " ## WELCOME TO KRAKOS HUB ## ".center(WIDTH, "-")
    print_row(title)
    print_row("Available Games :")
    last = len(options) - 1
    for i, option in enumerate(options):
        if i == last:
            print_row("")                  # empty row before QUIT
            label = f"0. {option}"
        else:
            label = f"{i + 1}. {option}"
        color = HIGHLIGHT if i == selected else NORMAL
        print_row(label, color)
    print_row("-" * WIDTH)

def read_key():
    key = getwch()
    if key in ("\x00", "\xe0"):          # arrow/function key: read its second character
        second = getwch()
        if second == "H":
            return "UP"
        if second == "P":
            return "DOWN"
        return ""                        # other special keys are ignored
    if key in AZERTY_ROW:
        return str((AZERTY_ROW.index(key) + 1) % 10)
    return key


def main():
    loaded_games = load_games()
    options = []
    for game in loaded_games:
        options.append(game.NAME)
    options.append("QUIT")

    menu_height = len(options) + 4
    selected = 0

    print("\033[2J\033[H", end="", flush=True) 
    draw_menu(options, selected)

    while True:
        previous = selected
        key = read_key()

        if key == "UP":
            selected = (selected - 1) % len(options)
        elif key == "DOWN":
            selected = (selected + 1) % len(options)
        elif key == "\r":                       # Enter (next step)
            if selected == len(options) - 1:
                return
            else:
                print("\033[2J\033[H", end="", flush=True)
                game = loaded_games[selected]
                try:
                    game.play()
                    print("Press any key to return to the menu")
                    read_key()
                except KeyboardInterrupt:
                    pass
                print("\033[2J\033[H", end="", flush=True)
                draw_menu(options, selected)
            
        elif key == "\x03" or key == "\x1b":    # Ctrl+C or Esc
            return
        elif key.isascii() and key.isdecimal():
            value = int(key)
            if value == 0:
                selected = len(options) - 1     # 0 = QUIT, the last row
            elif value <= len(loaded_games):
                selected = value - 1

        if selected != previous:                # redraw only when something changed
            print(f"\033[{menu_height}A", end="", flush=True)
            draw_menu(options, selected)


if __name__ == "__main__":
    main()