from pathlib import Path
from random import *

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

def play():
    # Game Loop
    game_solution = choose_a_solution()
    turn = 1
    while True:
        print(f"Turn {turn}, {7-turn} attempts left")
        game_guess = input("Choose a five letter word : ").lower()
        while True: 
            if is_valid(game_guess):
                break
            else:
                game_guess = input("Invalid word, please retry : ").lower()
        score = compare_guess_to_solution(game_solution, game_guess)
        print(score)
        if is_won(score):
            print(f"YOU WON !!! (in {turn} attempt, congratulations)")
            break
        elif turn == 6:
            print("YOU LOST !!!")
            break
        turn += 1

if __name__ == "__main__":
    play()