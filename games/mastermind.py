import random
from pathlib import Path
from msvcrt import getwch
from time import time
from datetime import datetime, timezone
import json
import secrets
from main import LOG_VERSION

NAME = "Mastermind"

color_list = ["r", "g", "b", "y", "o", "p"]
colors_value = {
    "r": "\033[48;2;231;76;60m\033[1;97m",
    "g": "\033[48;2;46;204;113m\033[1;97m",
    "b": "\033[48;2;52;152;219m\033[1;97m",
    "y": "\033[48;2;241;196;15m\033[1;97m",
    "o": "\033[48;2;230;126;34m\033[1;97m",
    "p": "\033[48;2;155;89;182m\033[1;97m",
}

def load_records():
    log_path = Path(__file__).parent /  "logs" / "game_logs.jsonl"
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

def generate_unique_id():
    existing_records = load_records()
    existing_ids = {record["id"] for record in existing_records if "id" in record}
    while True:
        new_id = secrets.token_hex(3)

        if new_id not in existing_ids:
            return new_id

def save_stat(result, duration, solution, guesses_list):
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    game_id = generate_unique_id()
    line = {"id": game_id, "v": LOG_VERSION, "date": date, "game": "Mastermind", "result": result, "duration": duration, "details": {"solution": "".join(solution), "guesses": guesses_list}}
    log_path = Path(__file__).parent /  "logs" / "game_logs.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with  open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")

def create_code(restricted=None):
    return random.choices(color_list, k=4)

def score(key, guess):
    temp_key = list(key)
    temp_guess = list(guess)
    right_pos = 0
    right_color = 0

    for i in range(4):
        if temp_guess[i] == temp_key[i]:
            right_pos += 1
            temp_key[i] = None
            temp_guess[i] = None

    for i in range(4):
        if temp_guess[i] is not None and temp_guess[i] in temp_key:
            right_color += 1
            temp_key[temp_key.index(temp_guess[i])] = None

    return (right_pos, right_color)

def read_combination(rows_below, starting_time, game_solution, guesses_list):
    colors = []
    message_shown = False
    draw_row(colors)
    while True:
        key = getwch()

        if message_shown:
            show_message("", rows_below)
            message_shown = False

        if key == "\x03" or key == "\x1b":     # Ctrl+C and Esc
            save_stat("abandoned", time() - starting_time, game_solution, guesses_list)
            raise KeyboardInterrupt
        elif key in ("\x00", "\xe0"):          # arrow/function key
            getwch()
        elif key == "\x08":                    # Backspace
            if colors:
                colors.pop()
        elif key == "\r":                      # Enter
            if len(colors) == 4:
                combination = "".join(colors)
                return combination
        elif key.isascii() and key.isalpha() and key.lower() in color_list:  # a letter
            if len(colors) < 4:
                colors.append(key.lower())

        draw_row(colors)

def show_message(text, rows_below):
    # go down to the line under the board, write the text, come back up
    print(f"\033[{rows_below}B\r\033[2K{text}\033[{rows_below}A", end="", flush=True)

def play():
    starting_time = time()
    guesses_list = []
    key = create_code()

    for _ in range(10):
        draw_row([])
        print()

    turn = 1
    while True:
        rows_below = 11 - turn                      # lines between the current row and the line under the board
        print(f"\033[{rows_below}A", end="")       # go up to the current row
        game_guess = read_combination(rows_below, starting_time, key, guesses_list)
        guesses_list.append(game_guess)
        points = score(key, game_guess)
        # add the right scoring to the right
        draw_row(game_guess, points)
        print(f"\033[{rows_below}B\r", end="", flush=True)

        if list(game_guess) == key:
            ending_time = time()
            save_stat("won", ending_time - starting_time, key, guesses_list)
            print(f"YOU WON !!! (in {turn} attempts and {ending_time - starting_time} seconds, congratulations)")
            break
        elif turn == 10:
            colored_solution = ""
            for char in key:
                colored_solution += f"{colors_value[char]} {char.upper()} \033[0m"
            save_stat("lost", time() - starting_time, key, guesses_list)
            print(f"YOU LOST !!! The code was {colored_solution}")
            break
        turn += 1

def draw_row(colors, scoring=None):
    tiles = ""
    for i in range(4):
        if i < len(colors):
            tiles += f"{colors_value[colors[i]]} {colors[i].upper()} \033[0m"
        else:
            tiles += "\033[48;2;40;40;42m   \033[0m"
    if scoring is None:
        tiles += "\033[48;2;231;76;60m   \033[0m"
        tiles += "\033[48;2;255;255;255m   \033[0m"
    else:
        tiles += f"\033[48;2;231;76;60m {scoring[0]} \033[0m"
        tiles += f"\033[48;2;255;255;255m\033[1m\033[38;2;30;30;30m {scoring[1]} \033[0m"
    print("\r" + tiles, end="", flush=True)

if __name__ == "__main__":
    play()