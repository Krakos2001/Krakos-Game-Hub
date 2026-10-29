from random import choice
from msvcrt import getwch, kbhit
from time import time, sleep, monotonic
from menu import WIDTH, print_row
from records import save_stat, get_best_score, load_records

ROWS = 10
COLUMNS = 10
TICK = 0.15            # seconds between two moves of the snake
DIRECTIONS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

EMPTY = "\033[48;2;40;40;42m   \033[0m"
BODY = "\033[48;2;46;204;113m   \033[0m"
FOOD = "\033[48;2;231;76;60m   \033[0m"

NAME = "Snake"
GAME_TYPE = "score"

def show_stats():
    records = [record for record in load_records() if record.get("game") == "Snake"]
    finished = [record for record in records if record.get("result") == "finished"]
    abandoned = len(records) - len(finished)
    scores = [record["details"]["score"] for record in finished]

    if len(scores) == 0:
        best_score = None
        average_score = None
        longest_game = None
    else:
        best_score = max(scores)
        average_score = sum(scores) / len(scores)
        longest_game = max(record["duration"] for record in finished)

    print("\033[2J\033[H", end="", flush=True)
    title = " ## SNAKE OVERVIEW ## ".center(WIDTH, "-")
    print_row(title)

    print_row(f"Games played : {len(records)}")
    print_row(f"Finished / Abandoned : {len(finished)} / {abandoned}")

    if best_score is None:
        print_row("Best score : n/a (No finished games)")
    else:
        print_row(f"Best score : {best_score}")

    if average_score is None:
        print_row("Average score : n/a (No finished games)")
    else:
        print_row(f"Average score : {average_score:.2f}")

    if longest_game is None:
        print_row("Longest game : n/a (No finished games)")
    else:
        print_row(f"Longest game : {longest_game:.1f}s")
    print_row("-" * WIDTH)

def read_keys():
    # returns the arrows waiting in the keyboard buffer, in order, and never blocks
    directions = []
    while kbhit():
        key = getwch()

        if key == "\x03" or key == "\x1b":     # Ctrl+C and Esc
            raise KeyboardInterrupt
        elif key in ("\x00", "\xe0"):          # arrow/function key
            new_key = getwch()
            if new_key == "H":
                directions.append("UP")
            elif new_key == "P":
                directions.append("DOWN")
            elif new_key == "K":
                directions.append("LEFT")
            elif new_key == "M":
                directions.append("RIGHT")
    return directions

def fill_queue(queue, direction):
    # keeps at most 2 turns waiting, and ignores the same direction or the opposite one
    for new_direction in read_keys():
        if len(queue) > 0:
            last = queue[-1]
        else:
            last = direction
        if len(queue) < 2 and new_direction != last and new_direction != OPPOSITE[last]:
            queue.append(new_direction)

def place_food(snake_body):
    # the food only appears on a free cell, None if the snake fills the whole board
    free_cells = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            if [row, column] not in snake_body:
                free_cells.append([row, column])
    if len(free_cells) == 0:
        return None
    return choice(free_cells)

def hits_itself(new_head, snake_body, eating):
    # if the snake doesn't eat, its tail moves away, so the tail cell is free
    if eating:
        return new_head in snake_body
    return new_head in snake_body[1:]

def draw(snake_body, food, score, best_score):
    lines = []
    for row in range(ROWS):
        line = ""
        for column in range(COLUMNS):
            if [row, column] in snake_body:
                line += BODY
            elif [row, column] == food:
                line += FOOD
            else:
                line += EMPTY
        lines.append(line)
    lines.append(f"\033[48;2;40;40;42m S C O R E : {score} / P R : {max(best_score, score)} \033[0m")
    print("\033[H" + "\n".join(lines), flush=True)

def dying(score, starting_time, best_score, message="You Died"):
    ending_time = time()
    while kbhit():
        getwch()
    save_stat("Snake", "finished", ending_time - starting_time, {"score": score})
    print(message)
    print(f"Score : {score}")
    if score > best_score:
        print(f"NEW HIGH SCORE ! (previous best : {best_score})")
    else:
        print(f"Best score : {best_score}")

def abandon(score, starting_time):
    ending_time = time()
    while kbhit():
        getwch()
    save_stat("Snake", "abandoned", ending_time - starting_time, {"score": score})
    print("Game abandoned")

def play():
    starting_time = time()
    best_score = get_best_score("Snake")       # read once, not at every tick
    score = 0

    snake_body = [[ROWS // 2, 1]]
    food = place_food(snake_body)
    direction = "RIGHT"
    queue = []

    print("\033[2J\033[H\033[?25l", end="", flush=True)     # clear the screen and hide the cursor
    try:
        next_tick = monotonic() + TICK
        while True:
            draw(snake_body, food, score, best_score)

            # wait for the next tick, reading the keys while we wait
            while monotonic() < next_tick:
                fill_queue(queue, direction)
                sleep(0.01)
            next_tick += TICK
            if next_tick < monotonic():        # the game froze for a moment: no burst of moves
                next_tick = monotonic() + TICK

            if len(queue) > 0:
                direction = queue.pop(0)
            row_change, column_change = DIRECTIONS[direction]
            new_head = [snake_body[-1][0] + row_change, snake_body[-1][1] + column_change]

            # out of the borders
            if new_head[0] < 0 or new_head[0] > ROWS - 1 or new_head[1] < 0 or new_head[1] > COLUMNS - 1:
                dying(score, starting_time, best_score)
                break

            eating = new_head == food
            if hits_itself(new_head, snake_body, eating):
                dying(score, starting_time, best_score)
                break

            snake_body.append(new_head)
            if eating:
                score += 1
                food = place_food(snake_body)
                if food is None:
                    dying(score, starting_time, best_score, "You filled the whole board !")
                    break
            else:
                # remove the last body part if it's not eating the food
                snake_body.pop(0)
    except KeyboardInterrupt:
        abandon(score, starting_time)
    finally:
        print("\033[?25h", end="", flush=True)       # show the cursor again

if __name__ == "__main__":
    play()