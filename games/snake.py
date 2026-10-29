from random import *
from msvcrt import getwch, kbhit
from time import time, sleep
from datetime import datetime, timezone
from pathlib import Path
import json
import secrets
from menu import LOG_VERSION

ROWS = 10  
COLUMNS = 10
DIRECTION_ORDER = {"UP":1, "RIGHT":2, "DOWN":3, "LEFT":4}

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

def save_stat(score, duration):
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    game_id = generate_unique_id()
    line = {"id": game_id, "v": LOG_VERSION, "date": date, "game": "Snake", "result": "Non-Binary GameMode", "duration": duration, "details": {"score": score}}
    log_path = Path(__file__).parent /  "logs" / "game_logs.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with  open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")

def read_key(starting_time, points):
    while kbhit():
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

def dying(score, starting_time):
    ending_time = time()
    while kbhit():
        getwch()
    save_stat(score, ending_time - starting_time)
    print("You Died")
    

def play():
    starting_time = time()
    game_map = []
    score = 0

    # generate the game maps
    for row in range(ROWS):
        game_map.append([])
        for column in range(COLUMNS):
            game_map[row].append("\033[48;2;40;40;42m   \033[0m")

    # pick the snake starting cordinate
    snake_row = 5
    snake_column = 1

    snake_body = []
    snake_body.append([snake_row, snake_column])

    # pick the food cordinate
    food_row = randint(0, ROWS - 1)
    food_column = randint(0, COLUMNS - 1)
    last_move = "RIGHT"

    while True:
        # if the snake in our of the borders, the game end
        if snake_row < 0 or snake_row > ROWS - 1 or snake_column < 0 or snake_column > COLUMNS - 1:
            dying(score, starting_time)
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
        print("\033[H", end="", flush=True)
        for row in game_map:
            print("".join(row))
        print("\n")

        sleep(0.15)
        move = read_key(starting_time, 0)

        if move is None:
            move = last_move

        if (DIRECTION_ORDER[last_move] - DIRECTION_ORDER[move]) % 4 == 2:
            move = last_move

        if move == "UP":
            if [snake_row - 1, snake_column] in snake_body:
                dying(score, starting_time)
                break
            snake_body.append([snake_row - 1, snake_column])
            snake_row -= 1
            if [food_row, food_column] in snake_body:
                score += 1
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                # remove the last body part if it's not eating the food
                snake_body.pop(0)
        
        elif move == "DOWN":
            if [snake_row + 1, snake_column] in snake_body:
                dying(score, starting_time)
                break
            snake_body.append([snake_row + 1, snake_column])
            snake_row += 1
            if [food_row, food_column] in snake_body:
                score += 1
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)
        
        elif move == "LEFT":
            if [snake_row, snake_column - 1] in snake_body:
                dying(score, starting_time)
                break
            snake_body.append([snake_row, snake_column - 1])
            snake_column -= 1
            if [food_row, food_column] in snake_body:
                score += 1
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)
        
        elif move == "RIGHT":
            if [snake_row, snake_column + 1] in snake_body:
                dying(score, starting_time)
                break
            snake_body.append([snake_row, snake_column + 1])
            snake_column += 1
            if [food_row, food_column] in snake_body:
                score += 1
                while [food_row, food_column] in snake_body:
                    food_row = randint(0, ROWS - 1)
                    food_column = randint(0, COLUMNS - 1)
            else:
                snake_body.pop(0)

        last_move = move


if __name__ == "__main__":
    play()