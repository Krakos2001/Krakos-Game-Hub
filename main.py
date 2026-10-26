import importlib
import pkgutil
import games
from msvcrt import getwch

WIDTH = 49
RESET = "\033[0m"
NORMAL = "\033[48;2;58;58;60m\033[1;97m"                 # dark gray, white bold text
HIGHLIGHT = "\033[48;2;200;200;200m\033[1m\033[38;2;30;30;30m"  # light gray, dark bold text


def load_games():
    loaded_games = []
    for item in pkgutil.iter_modules(games.__path__):
        loaded_games.append(importlib.import_module(f"games.{item.name}"))
    return loaded_games


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


def main():
    loaded_games = load_games()
    options = []
    for game in loaded_games:
        options.append(game.NAME)
    options.append("QUIT")
    MENU_HEIGHT = len(options) + 4
    draw_menu(options, 0)
    selected = 1
    while True:
        key = getwch()
        if key.isascii():
            selected = (selected + 1) % len(options)
            print(f"\033[{MENU_HEIGHT}A", end="", flush=True)
            draw_menu(options, selected)

if __name__ == "__main__":
    main()
