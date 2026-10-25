from pathlib import Path
from random import *

def choose_a_solution():
    path = Path(__file__).parent / "wordle.txt"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    return lines[randint(1, len(lines))]

def compare_guess_to_solution(guess, solution):
    solution_pool = []
    for char in solution:
        solution.append(char)
    score = {1:"",2:"",3:"",4:"",5:""}
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            score[i] = "green"
            solution_pool.pop(solution[i])
    for i in range(len(guess)):
        if guess[i] in solution_pool:
                 