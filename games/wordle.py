from pathlib import Path
from random import *
from msvcrt import getwch
from time import time
from datetime import datetime, timezone
import json
import secrets
from menu import LOG_VERSION

NAME = "Wordle"

# Create a list of accepted word
path = Path(__file__).parent /  "wordlist_fives.txt"
with open(path, "r", encoding="utf-8") as f:
    accepted = f.read().splitlines()

def is_valid(guess):
    return guess in accepted

def choose_a_solution():
    path = Path(__file__).parent / "wordle.txt"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    while True:
        potential_solution = lines[randint(0, len(lines)-1)]
        if potential_solution in accepted:    
            return potential_solution 

def compare_guess_to_solution(solution, guess):
    solution_pool = []
    for char in solution:
        solution_pool.append(char)
    score = {0:"",1:"",2:"",3:"",4:""}
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            score[i] = "green"
            solution_pool.remove(guess[i])
    for i in range(len(guess)):
        if guess[i] in solution_pool and score[i] != "green":
                score[i] = "yellow"
                solution_pool.remove(guess[i])
        elif score[i] != "green":
            score[i] = "gray"
    return score

def is_won(score):
    for i in score.values():
        if i != "green":
            return False
    return True

def word_in_color(word, score):
    colored_word = ""
    for i in range(len(score)):
        if score[i] == "green":
            letter = word[i]
            colored_word += f"\033[48;2;83;141;78m\033[1;97m {letter.upper()} \033[0m"
        elif score[i] == "yellow":
            letter = word[i]
            colored_word += f"\033[48;2;181;159;59m\033[1;97m {letter.upper()} \033[0m"
        elif score[i] == "gray":
            letter = word[i]
            colored_word += f"\033[48;2;58;58;60m\033[1;97m {letter.upper()} \033[0m"
    return colored_word
  
def show_message(text, rows_below):
    # go down to the line under the board, write the text, come back up
    print(f"\033[{rows_below}B\r\033[2K{text}\033[{rows_below}A", end="", flush=True)

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
    line = {"id": game_id, "v": LOG_VERSION, "date": date, "game": "Wordle", "result": result, "duration": duration, "details": {"solution": solution, "guesses": guesses_list}}
    log_path = Path(__file__).parent /  "logs" / "game_logs.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with  open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")

def read_word(rows_below, starting_time, game_solution, guesses_list):
    letters = []
    message_shown = False
    draw_row(letters)
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
            if letters:
                letters.pop()
        elif key == "\r":                      # Enter
            if len(letters) == 5:
                word = "".join(letters)
                if is_valid(word):
                    return word
                show_message("Not in word list", rows_below)
                message_shown = True
        elif key.isascii() and key.isalpha():  # a letter
            if len(letters) < 5:
                letters.append(key.lower())

        draw_row(letters)

def play():
    starting_time = time()
    guesses_list = []
    game_solution = choose_a_solution()

    # draw the empty board: 6 rows of empty tiles
    for _ in range(6):
        draw_row([])
        print()

    turn = 1
    while True:
        rows_below = 7 - turn                      # lines between the current row and the line under the board
        print(f"\033[{rows_below}A", end="")       # go up to the current row
        game_guess = read_word(rows_below, starting_time, game_solution, guesses_list)
        guesses_list.append(game_guess)
        score = compare_guess_to_solution(game_solution, game_guess)
        # repaint the row in colors, then go back down under the board
        print("\r" + word_in_color(game_guess, score) + f"\033[{rows_below}B\r", end="", flush=True)

        if is_won(score):
            ending_time = time()
            save_stat("won", ending_time - starting_time, game_solution, guesses_list)
            print(f"YOU WON !!! (in {turn} attempts and {ending_time - starting_time} seconds, congratulations)")
            break
        elif turn == 6:
            colored_solution = ""
            for char in game_solution:
                colored_solution += f"\033[48;2;83;141;78m\033[1;97m {char.upper()} \033[0m"
            save_stat("lost", time() - starting_time, game_solution, guesses_list)
            print(f"YOU LOST !!! The word was {colored_solution}")
            break
        turn += 1

def draw_row(letters):
    tiles = ""
    for i in range(5):
        if i < len(letters):
            tiles += f"\033[48;2;86;87;88m\033[1;97m {letters[i].upper()} \033[0m"
        else:
            tiles += "\033[48;2;40;40;42m   \033[0m"
    print("\r" + tiles, end="", flush=True)

if __name__ == "__main__":
    play()