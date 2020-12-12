#!/usr/bin/env python3
#
# ./day03.py < day03.input.tx
#

import sys

forest = []
for line in sys.stdin:
    forest.append(line.strip())


def run_tobbogan(forest):
    encounters = 0
    column = 0
    grid_width = len(forest[0])

    for row in forest:
        print(row)
        if row[column] == "#":
            verdict = "X"
            encounters += 1
        else:
            verdict = "O"
        print((" " * column) + verdict)
        column = (column + 3) % grid_width

    return encounters


answer = run_tobbogan(forest)
print(f"Part I Answer: {answer}")

answer = None
print(f"Part II Answer: {answer}")
