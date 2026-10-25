from pathlib import Path
from random import *

NAME = "Wordle"
# Create a list of accepted word
path = Path(__file__).parent / "wordlist_fives.txt"
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
            colored_word += f"\033[48;2;83;141;78m\033[1;97m {letter} \033[0m"
        elif score[i] == "yellow":
            letter = word[i]
            colored_word += f"\033[48;2;181;159;59m\033[1;97m {letter} \033[0m"
        elif score[i] == "gray":
            letter = word[i]
            colored_word += f"\033[48;2;58;58;60m\033[1;97m {letter} \033[0m"
    return colored_word
  
def play():
    # Game Loop
    game_solution = choose_a_solution()
    turn = 1
    while True:
        print(f"Turn {turn}, {7-turn} attempts left")
        game_guess = input("Choose a five letter word : \n").lower().strip()
        while True: 
            if is_valid(game_guess):
                break
            else:
                game_guess = input("Invalid word, please retry : \n").lower().strip()
        score = compare_guess_to_solution(game_solution, game_guess)
        print(f"\033[A\033[2K{word_in_color(game_guess, score)}")
        if is_won(score):
            print(f"YOU WON !!! (in {turn} attempts, congratulations)")
            break
        elif turn == 6:
            colored_solution = ""
            for char in game_solution:
                colored_solution += f"\033[48;2;83;141;78m\033[1;97m {char} \033[0m"
            print(f"YOU LOST !!!, the word was {colored_solution}")
            break
        turn += 1

if __name__ == "__main__":
    play()