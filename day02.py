#!/usr/bin/env python3
#
# ./day02.py < day02.input.tx
#

import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())


def parse_old_policy(line):
    policy_str, letter_str, password = line.split(' ')
    letter = letter_str[0]
    low, high = tuple(map(int, policy_str.split('-')))
    policy = range(low, high + 1)
    return (password, letter, policy)


def validate_old_policy(password, letter, policy):
    count = len(list(filter(lambda c: c == letter, password)))
    verdict = count in policy
    print(f"verdict={verdict} letter={letter} count={count} policy={policy} password={password}")
    return verdict


def count_old_valid_passwords(lines):
    def _validate_line(line):
        password, letter, policy = parse_old_policy(line)
        return validate_old_policy(password, letter, policy)
    valid = filter(_validate_line, lines)
    return len(list(valid))


answer = count_old_valid_passwords(lines)
print(f"Part I Answer: {answer}")

def parse_policy(line):
    policy_str, letter_str, password = line.split(' ')
    letter = letter_str[0]
    low, high = tuple(map(int, policy_str.split('-')))
    policy = (low - 1, high - 1)
    return (password, letter, policy)


def validate_policy(password, letter, indexes):
    valid = filter(lambda index: password[index] == letter, indexes)
    count = len(list(valid))
    verdict = count == 1
    print(f"verdict={verdict} letter={letter} count={count} indexes={indexes} password={password}")
    return verdict


def count_valid_passwords(lines):
    def _validate_line(line):
        password, letter, policy = parse_policy(line)
        return validate_policy(password, letter, policy)
    valid = filter(_validate_line, lines)
    return len(list(valid))


answer = count_valid_passwords(lines)
print(f"Part II Answer: {answer}")
