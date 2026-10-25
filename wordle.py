from pathlib import Path
from random import *

def choose_a_solution():
    path = Path(__file__).parent / "wordle.txt"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    return lines[randint(1, len(lines))]

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
print(compare_guess_to_solution("crane", "cloak"))
print(compare_guess_to_solution("apple", "paper"))