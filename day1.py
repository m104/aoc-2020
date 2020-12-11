#!/usr/bin/env python3
#
# ./day1.py < day1.input.tx
#

import sys
from functools import reduce
from math import ceil

TARGET = 2020

numbers = []
for line in sys.stdin:
    numbers.append(int(line.strip()))

numbers = sorted(numbers)
print(numbers)

iterations = 0

def bsearch(target, collection, left, right):
  global iterations
  iterations += 1
  if left == right:
    return right
  
  test = ceil((right - left) / 2) + left
  value = collection[test]
  print(f"bsearch: target={target} left={left} test={test} right={right} value={value}")
  if value == target:
    return test
  if value > target:
    return bsearch(target, collection, left, test - 1)
  else:
    return bsearch(target, collection, test + 1, right)

def find_pair_positions(target, collection, left, right):
  base = collection[left]
  test = bsearch(target - base, collection, left, right)
  value = collection[test]
  total = base + value
  print(f"find_pair_positions: target={target} left={left} test={test} right={right} diff={total - target}")
  if total == target:
    return (left, test)
  else:
    return find_pair_positions(target, collection, left + 1, test)

positions = find_pair_positions(2020, numbers, 0, len(numbers) - 1)
pair = (numbers[positions[0]], numbers[positions[1]])
print(f"iterations={iterations} pair={pair}")
print(f"** Part I answer: {pair[0] * pair[1]}")

iterations = 0
def find_triplet_positions(target, collection):
  left = 0
  right = len(collection) - 1

  while True:
    base = collection[left]
    pair_positions = find_pair_positions(target - base, collection, left + 1, right)
    total = base + collection[pair_positions[0]] + collection[pair_positions[1]]
    if total == target:
      return (left, pair_positions[0], pair_positions[1])
    left += 1

positions = find_triplet_positions(2020, numbers)
values = list(map(lambda i: numbers[i], positions))
product = reduce(lambda x, y: x * y, values)
print(f"iterations={iterations} values={values}")
print(f"** Part II answer: {product}")
