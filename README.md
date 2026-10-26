# Krakos Game Hub

A terminal hub for mini-games, written in Python. Pick a game from an interactive menu, play it, and come back. The first game is a **Wordle** where you type directly into the tiles, just like the real thing.

> Made for [Pixl](https://pixl.hackclub.com) by Hack Club.

![Hub menu](images/menu.png)
![Wordle board](images/wordle.png)

## Features

- **Interactive menu**: move with the arrow keys or jump to a game with its number, then press Enter.
- **Automatic game discovery**: drop a new game in the `games/` folder and it shows up in the menu by itself.
- **Wordle with a live board**: six rows of tiles, you type inside the tiles, Backspace works, invalid words are refused, and the row turns green, yellow or gray when you validate.
- **Two word lists**: a smaller list of common words for the solutions, and a much larger one for the words you are allowed to guess.
- **Colors with ANSI escape codes**: no external libraries, only Python's standard library.

## Requirements

- **Windows only** for now, because key presses are read with the `msvcrt` module.
- Python 3.13 (the version it was tested with).
- Run it in a real terminal such as Windows Terminal, PowerShell or the VS Code integrated terminal. The VS Code *Output* panel does not work.
- Make the terminal window tall enough to show the whole menu and the six-row board (about 12 lines is safe).

## How to run

```
git clone https://github.com/Krakos2001/Krakos-Game-Hub.git
cd Krakos-Game-Hub
python main.py
```

Run it from the project folder, so Python can find the `games` package.

## Controls

### In the hub

| Key | Action |
|---|---|
| Up / Down arrows | Move the highlight |
| `1`-`9` | Jump to that game |
| `0` | Jump to QUIT |
| Enter | Launch the selected game (or quit) |
| Esc / Ctrl+C | Quit the hub |

On a French AZERTY keyboard, the top row keys (`&`, `é`, `"`, `'`, `(`, `-`, `è`, `_`, `ç`) work as `1` to `9` without pressing Shift.

### In Wordle

| Key | Action |
|---|---|
| Letters | Type a letter in the current row |
| Backspace | Delete the last letter |
| Enter | Validate the word (it must be 5 letters and in the word list) |
| Ctrl+C | Leave the game and go back to the hub |

You have six attempts. After each guess:

- **Green**: the letter is in the right place.
- **Yellow**: the letter is in the word, but in another place.
- **Gray**: the letter is not in the word (or all its copies are already accounted for).

## Project structure

```
Krakos-Game-Hub/
├── main.py              # the hub: finds the games and shows the menu
└── games/
    ├── __init__.py      # makes games/ a package (empty)
    ├── wordle.py        # the Wordle game
    ├── wordle.txt       # solution words
    └── wordlist_fives.txt   # accepted guesses
```

## Adding a game

Every game is a Python file in `games/` that has two things:

1. a variable `NAME`, the text shown in the menu
2. a function `play()`, which the hub calls when the player picks the game

```python
# games/my_game.py
NAME = "My Game"

def play():
    ...
```

Restart the hub and "My Game" appears in the menu. If your game needs data files, put them in `games/` and build their paths with `Path(__file__).parent`, so they are found wherever the hub is launched from.

## Credits and data

- The word lists come from [John Burkardt's word datasets](https://people.sc.fsu.edu/~jburkardt/datasets/words/): `wordlist_fives.txt` for the accepted guesses and `wordle.txt` for the solutions. Check the terms on that page before reusing them.
- Wordle is a game created by Josh Wardle and now owned by The New York Times. This project is a fan-made imitation and is not affiliated with or endorsed by the NYT.
- Built as part of [Hack Club](https://hackclub.com)'s Pixl.

## Status and ideas

Working now: the hub, Wordle, and the keyboard navigation.

Ideas for later:

- More mini-games
- Esc to go back to the hub from inside a game
- Cross-platform key reading (Mac and Linux)
- A player name and a score shared between games
