#!/usr/bin/env python3
#
# ./day03.py < day03.input.tx
#

import sys
from functools import reduce

forest = []
for line in sys.stdin:
    forest.append(line.strip())


def run_tobbogan(forest, slope):
    encounters = 0
    row = 0
    column = 0
    grid_width = len(forest[0])
    forest_height = len(forest)

    while row < forest_height:
        trees = forest[row]
        if trees[column] == "#":
            verdict = "X"
            encounters += 1
        else:
            verdict = "O"
        print(trees)
        print((" " * column) + verdict)
        column = (column + slope[0]) % grid_width
        row += slope[1]

    return encounters


answer = run_tobbogan(forest, (3, 1))
print(f"Part I Answer: {answer}")

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
encounters = [run_tobbogan(forest, slope) for slope in slopes]
print(f"encouters={encounters}")
answer = reduce(lambda e1, e2: e1 * e2, encounters)
print(f"Part II Answer: {answer}")
