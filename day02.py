#!/usr/bin/env python3
#
# ./day02.py < day02.input.tx
#

import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())


def parse_line(line):
    policy_str, letter_str, password = line.split(' ')
    letter = letter_str[0]
    low, high = tuple(map(int, policy_str.split('-')))
    policy = range(low, high + 1)
    return (password, letter, policy)


def validate_policy(password, letter, policy):
    count = len(list(filter(lambda c: c == letter, password)))
    verdict = count in policy
    print(f"verdict={verdict} letter={letter} count={count} polict={policy} password={password}")
    return verdict


def count_valid_passwords(lines):
    def _validate_line(line):
        password, letter, policy = parse_line(line)
        return validate_policy(password, letter, policy)
    valid = filter(_validate_line, lines)

    return len(list(valid))


answer = count_valid_passwords(lines)
print(f"Part I Answer: {answer}")