from menu import WIDTH, run_menu, print_row, read_key
from records import load_records

def filter_records(records, filters, filter_category):
    matches = [record for record in records if record.get(filter_category) == filters]
    return matches

def compute_stat(records, game=None):

    if game is not None:
        records = filter_records(records, game, "game")

    games_played = len(records)
    
    won = len(filter_records(records, "won", "result"))

    won_records = filter_records(records, "won", "result")  

    lost = len(filter_records(records, "lost", "result"))

    abandoned = len(filter_records(records, "abandoned", "result"))

    if won + lost == 0:
        win_rate = None
    else:
        win_rate = won / (won + lost)

    if games_played == 0:
        abandon_rate = None
    else:
        abandon_rate = abandoned / games_played
    
    if won == 0:
        avg_attempts_per_win = None
    else:
        avg_attempts_per_win = sum(len(record["details"]["guesses"]) for record in won_records) / won

    if won == 0:
        fastest_win = None
        fastest_win_time = None
    else:
        fastest_win = min(won_records, key=lambda record: record["duration"])
        fastest_win_time = fastest_win["duration"]

    return {"games_played": games_played, "won": won, "lost": lost, "abandoned": abandoned, "win_rate": win_rate, "abandon_rate": abandon_rate, "avg_attempts_per_win": avg_attempts_per_win, "fastest_win": fastest_win, "fastest_win_time": fastest_win_time}

def show_stats(game=None, win_loss_games=None):
    records = load_records()
    all_records = records
    if game is None and win_loss_games is not None:
        # the global win stats only count the games that have a win or a loss
        records = [record for record in records if record.get("game") in win_loss_games]
    stats = compute_stat(records, game)
    is_global = game is None
    if is_global:
        game = "Global"

    print("\033[2J\033[H", end="", flush=True) 
    title = f" ## {game.upper()} OVERVIEW ## ".center(WIDTH, "-")
    print_row(title)

    if is_global:
        games_count = {}
        for record in all_records:
            name = record.get("game")
            games_count[name] = games_count.get(name, 0) + 1
        print_row(f"Total games played : {len(all_records)}")
        if len(games_count) == 0:
            print_row("Most played game : n/a (No played games)")
        else:
            most_played = max(games_count, key=games_count.get)
            print_row(f"Most played game : {most_played} ({games_count[most_played]})")
        print_row("Win / Loss games only :")

    print_row(f"Games played : {stats["games_played"]}")
    print_row(f"Won / Lost / Abandoned : {stats["won"]} / {stats["lost"]} / {stats["abandoned"]}")
    
    if stats["win_rate"] is None:
        print_row(f"Win rate : n/a (No finished games)")
    else:
        print_row(f"Win rate : {stats["win_rate"] * 100:.2f}% ({stats["won"]}/{stats["won"] + stats["lost"]})")
    
    if stats["abandon_rate"] is None:
        print_row(f"Abandon rate : n/a (No played games)")
    else:
        print_row(f"Abandon rate : {stats["abandon_rate"] * 100:.2f}% ({stats["abandoned"]}/{stats["games_played"]})")
    
    if stats["avg_attempts_per_win"] is None:
        print_row(f"Avg attempts per win : n/a (No won games)")
    else:
        print_row(f"Avg attempts per win : {stats["avg_attempts_per_win"]:.2f}")

    if stats["fastest_win_time"] is None:
        print_row(f"Fastest win : n/a (No won games)")
    else:
        print_row(f"Fastest win : {stats["fastest_win_time"]:.3f}s")
    print_row("-" * WIDTH)
    

def stats_menu(loaded_games):
    options = ["Global"]
    win_loss_games = []
    for game in loaded_games:
        options.append(game.NAME)
        if getattr(game, "GAME_TYPE", "win_loss") == "win_loss":
            win_loss_games.append(game.NAME)
    options.append("BACK")

    last_position = 0
    title = " ## STATISTICS ## ".center(WIDTH, "-")
    while True:
        choice = run_menu(title, options, "Available Stats :", last_position)
        if choice is None:
            return
        last_position = choice
        print("\033[2J\033[H", end="", flush=True)
        try:
            if choice == 0:
                show_stats(None, win_loss_games)
            elif hasattr(loaded_games[choice - 1], "show_stats"):
                loaded_games[choice - 1].show_stats()
            else:
                show_stats(loaded_games[choice - 1].NAME)
            print("Press any key to return to the menu")
            read_key()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    show_stats()