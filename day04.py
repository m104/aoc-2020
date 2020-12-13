#!/usr/bin/env python3
#
# Debug:
#   ./day04.py < day04.input.txt
# Run:
#   ./day04.py < day04.input.txt 2>/dev/null

import re
import sys
from functools import partial

lines = []
for line in sys.stdin:
    lines.append(line.strip())

REQUIRED_FIELDS = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
}


def group_input_to_passports(lines):
    groups = []
    group = []
    for line in lines:
        if line:
            group.append(line)
        else:
            groups.append(group)
            group = []

    groups.append(group)
    return groups


def extract_passport_fields(line):
    return dict(list(map(lambda p: tuple(p.split(":")), line.split(" "))))


def assemble_passport_fields(lines):
    passport = dict()
    for line in lines:
        passport.update(extract_passport_fields(line))
    return passport


def validate_passport_required_fields(passport):
    keys = set(passport.keys())
    missing_keys = REQUIRED_FIELDS - keys
    if missing_keys:
        print(f"missing_keys={missing_keys} passport={passport!r}", file=sys.stderr)
    return not missing_keys


def count_valid_passports(lines):
    passports = map(assemble_passport_fields, group_input_to_passports(lines))
    valid = list(filter(validate_passport_required_fields, passports))
    return len(valid)


answer = count_valid_passports(lines)
print(f"Part I Answer: {answer}")


def validate_numeric_range(min, max, value):
    return int(value) in range(min, max + 1)


def validate_height(value):
    measurement = value[0:-2]
    unit = value[-2:]
    if unit == "in":
        lower, upper = 59, 76
    elif unit == "cm":
        lower, upper = 150, 193
    else:
        return False
    return validate_numeric_range(lower, upper, measurement)


HAIR_COLOR_PATTERN = re.compile("^#[0-9a-f]{6}$")
EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
PASSPORT_ID_PATTERN = re.compile("^[0-9]{9}$")


def validate_hair_color(value):
    return HAIR_COLOR_PATTERN.match(value)


def validate_eye_color(value):
    return value in EYE_COLORS


def validate_passport_id(value):
    return PASSPORT_ID_PATTERN.match(value)


VALIDATIONS = {
    "byr": partial(validate_numeric_range, 1920, 2002),
    "iyr": partial(validate_numeric_range, 2010, 2020),
    "eyr": partial(validate_numeric_range, 2020, 2030),
    "hgt": partial(validate_height),
    "hcl": partial(validate_hair_color),
    "ecl": partial(validate_eye_color),
    "pid": partial(validate_passport_id),
}


def validate_passport_fields(passport):
    for field, validation_fn in VALIDATIONS.items():
        value = passport[field]
        verdict = validation_fn(value)
        if not verdict:
            print(f"failed_field={field} value={value}", file=sys.stderr)
            return False
    return True


def count_valid_passports_strictly(lines):
    passports = map(assemble_passport_fields, group_input_to_passports(lines))
    filled = filter(validate_passport_required_fields, passports)
    valid = filter(validate_passport_fields, filled)
    return len(list(valid))


answer = count_valid_passports_strictly(lines)
print(f"Part II Answer: {answer}")
