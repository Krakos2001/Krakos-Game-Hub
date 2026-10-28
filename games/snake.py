from random import *
from msvcrt import getwch
from time import time
from datetime import datetime, timezone
from pathlib import Path
import json
import secrets
from menu import LOG_VERSION

ROWS = 10
COLUMNS = 10

NAME = "Snake"

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

def read_key(starting_time, points):
    while True:
        key = getwch()

        if key == "\x03" or key == "\x1b":     # Ctrl+C and Esc
            save_stat("abandoned", time() - starting_time, points)
            raise KeyboardInterrupt
        elif key in ("\x00", "\xe0"):          # arrow/function key
            new_key = getwch()
            if new_key == "H":
                return "UP"
            elif new_key == "P":
                return "DOWN"
            elif new_key == "K":
                return "LEFT"
            elif new_key == "M":
                return "RIGHT"
            else:
                return
        elif key == "\r":                      # Enter
            pass

def play():
    starting_time = time()
    game_map = []

    # generate the game maps
    for row in range(ROWS):
        game_map.append([])
        for column in range(COLUMNS):
            game_map[row].append("\033[48;2;40;40;42m   \033[0m")

    # pick the snake starting cordinate
    snake_row = randint(0, ROWS - 1)
    snake_column = randint(0, COLUMNS - 1)

    snake_body = []
    snake_body.append([snake_row, snake_column])

    # pick the food cordinate
    food_row = randint(0, ROWS - 1)
    food_column = randint(0, COLUMNS - 1)

    while True:
        # if the snake in our of the borders, the game end
        if snake_row < 0 or snake_row > ROWS - 1 or snake_column < 0 or snake_column > COLUMNS - 1:
            print("You lose!, since you can't teleport trough the walls")
            break
        # set the snake body
        for body_part in snake_body:
            game_map[body_part[0]][body_part[1]] = "\033[48;2;46;204;113m   \033[0m"
        
        # set the food
        game_map[food_row][food_column] = "\033[48;2;231;76;60m   \033[0m"
        for row in range(ROWS):
            for column in range(COLUMNS):
                if [row, column] not in snake_body and [row, column] != [food_row, food_column]:
                    game_map[row][column] = "\033[48;2;40;40;42m   \033[0m"

        # print the game map
        for row in game_map:
            print("".join(row))
        print("\n")
        
        move = input("Enter your move: ")
        if move == "q":
            break
        elif move == "w":
            if [snake_row - 1, snake_column] in snake_body:
                print("You died!")
                break
            snake_body.append([snake_row - 1, snake_column])
            snake_row -= 1
            if [food_row, food_column] in snake_body:
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                # remove the last body part if it's not eating the food
                snake_body.pop(0)
        
        elif move == "s":
            if [snake_row + 1, snake_column] in snake_body:
                print("You died!")
                break
            snake_body.append([snake_row + 1, snake_column])
            snake_row += 1
            if [food_row, food_column] in snake_body:
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)
        
        elif move == "a":
            if [snake_row, snake_column - 1] in snake_body:
                print("You died!")
                break
            snake_body.append([snake_row, snake_column - 1])
            snake_column -= 1
            if [food_row, food_column] in snake_body:
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)
        
        elif move == "d":
            if [snake_row, snake_column + 1] in snake_body:
                print("You died!")
                break
            snake_body.append([snake_row, snake_column + 1])
            snake_column += 1
            if [food_row, food_column] in snake_body:
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)
        
        else:
            print("Invalid move!")
            continue

if __name__ == "__main__":
    play()