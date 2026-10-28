import importlib
import pkgutil
import games
from menu import run_menu, read_key, WIDTH
from stats import stats_menu

def load_games():
    loaded_games = []
    for item in pkgutil.iter_modules(games.__path__):
        loaded_games.append(importlib.import_module(f"games.{item.name}"))
    return loaded_games

def main():
    loaded_games = load_games()
    options = []
    for game in loaded_games:
        options.append(game.NAME)
    options.append("Stats")
    options.append("QUIT")

    last_position = 0
    title = " ## WELCOME TO KRAKOS HUB ## ".center(WIDTH, "-")
    while True:
        choice = run_menu(title, options, "Available Modules :", last_position)
        if choice is None:
            return
        last_position = choice
        if choice == len(loaded_games):
            stats_menu(load_games())

        else:
            game = loaded_games[choice]
            print("\033[2J\033[H", end="", flush=True)
            try:
                game.play()
                print("Press any key to return to the menu")
                read_key()
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    main()