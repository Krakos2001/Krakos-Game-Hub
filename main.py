import importlib
import pkgutil
import games

WIDTH = 49

def load_games():
    loaded_games = []
    for item in pkgutil.iter_modules(games.__path__):
        loaded_games.append(importlib.import_module(f"games.{item.name}"))
    return loaded_games

def initialise():
    loaded_games = load_games()
    print()
    print("\033[48;2;58;58;60m\033[1;97m---------- ## WELCOME TO KRAKOS HUB ## ----------\033[0m")
    print("\033[48;2;58;58;60m\033[1;97mAvailable Games :                                \033[0m")
    for i, game in enumerate(loaded_games, 1):
        line = f"{i}. {game.NAME}"
        print(f"\033[48;2;58;58;60m\033[1;97m{line:<{WIDTH}}\033[0m")
    empty_row = " " * WIDTH
    print(f"\033[48;2;58;58;60m\033[1;97m{empty_row}\033[0m")
    print(f"\033[48;2;58;58;60m\033[1;97m{"0. QUIT":<{WIDTH}}\033[0m")
    print("\033[48;2;58;58;60m\033[1;97m-------------------------------------------------\033[0m")
    print()

initialise()