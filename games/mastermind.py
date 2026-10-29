import random
from msvcrt import getwch
from time import time
from records import save_stat, get_best_win_time

NAME = "Mastermind"
GAME_TYPE = "win_loss"

color_list = ["r", "g", "b", "y", "o", "p"]
colors_value = {
    "r": "\033[48;2;231;76;60m\033[1;97m",
    "g": "\033[48;2;46;204;113m\033[1;97m",
    "b": "\033[48;2;52;152;219m\033[1;97m",
    "y": "\033[48;2;241;196;15m\033[1;97m",
    "o": "\033[48;2;230;126;34m\033[1;97m",
    "p": "\033[48;2;155;89;182m\033[1;97m",
}

last_line_of_board = ""
for values in colors_value:
    last_line_of_board += f"{colors_value[values]} {values.upper()} \033[0m"

def create_code():
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
            save_stat("Mastermind", "abandoned", time() - starting_time, {"solution": "".join(game_solution), "guesses": guesses_list})
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
    print("\033[48;2;40;40;42m C O L O R S : \033[0m")
    print(last_line_of_board)
    

    turn = 1
    while True:
        rows_below = 13 - turn                      # lines between the current row and the line under the board
        print(f"\033[{rows_below}A", end="")       # go up to the current row
        game_guess = read_combination(rows_below, starting_time, key, guesses_list)
        guesses_list.append(game_guess)
        points = score(key, game_guess)
        # add the right scoring to the right
        draw_row(game_guess, points)
        print(f"\033[{rows_below}B\r", end="", flush=True)

        if list(game_guess) == key:
            ending_time = time()
            best_time = get_best_win_time("Mastermind")
            save_stat("Mastermind", "won", ending_time - starting_time, {"solution": "".join(key), "guesses": guesses_list})
            print(f"YOU WON !!! (in {turn} attempts and {ending_time - starting_time:.1f} seconds, congratulations)")
            if best_time is not None:
                if ending_time - starting_time < best_time:
                    print(f"NEW TIME RECORD ! (previous best : {best_time:.1f}s)")
                else:
                    print(f"Best time : {best_time:.1f}s")
            break
        elif turn == 10:
            colored_solution = ""
            for char in key:
                colored_solution += f"{colors_value[char]} {char.upper()} \033[0m"
            save_stat("Mastermind", "lost", time() - starting_time, {"solution": "".join(key), "guesses": guesses_list})
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