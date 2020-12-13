#!/usr/bin/env python3
#
# Debug:
#   ./day12.py < day12.input.txt
# Run:
#   ./day12.py < day12.input.txt 2>/dev/null

import sys

# E, S, W, N
cardinals = [(1, 0), (0, -1), (-1, 0), (0, 1)]
cardinals_by_action = {
    "E": cardinals[0],
    "S": cardinals[1],
    "W": cardinals[2],
    "N": cardinals[3],
}


def parse_instruction(instruction):
    action = instruction[0]
    value = int(instruction[1:])
    return (action, value)


def vec_sum(vec1, vec2):
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])


def vec_scale(vec, scale):
    return (vec[0] * scale, vec[1] * scale)


def vec_rotate(vec, direction):
    """direction: 'R' or 'L' """
    if direction == "L":
        # (1, 13) -> (-13, 1)
        return (-vec[1], vec[0])
    else:
        # (-13, 1) -> (1, 13)
        return (vec[1], -vec[0])


def apply_action(position, pointing, action, value):
    print(f"position={position} pointing={pointing}", file=sys.stderr)
    print(f"action={action} value={value}", file=sys.stderr)
    if action in {"L", "R"}:
        # Rightward
        increment = 1
        if action == "L":
            increment = -1
        steps = int(value / 90)
        print(f"  increment={increment} steps={steps}", file=sys.stderr)
        pointing = (pointing + (increment * steps)) % len(cardinals)
        return (position, pointing)
    elif action in {"E", "S", "W", "N"}:
        cardinal = cardinals_by_action.get(action)
    else:
        cardinal = cardinals[pointing]
    vec = vec_scale(cardinal, value)
    position = vec_sum(position, vec)

    return (position, pointing)


instructions = []
for line in sys.stdin:
    instructions.append(line.strip())

position = (0, 0)
pointing = 0
for instruction in instructions:
    action, value = parse_instruction(instruction)
    position, pointing = apply_action(position, pointing, action, value)

print(f"PART I: Final position: {position}", file=sys.stderr)
distance = abs(position[0]) + abs(position[1])
print(f"PART I: Manhattan distance: {distance}")


waypoint = (10, 1)
position = (0, 0)

for instruction in instructions:
    action, value = parse_instruction(instruction)
    print(f"position={position} waypoint={waypoint}", file=sys.stderr)
    print(f"action={action} value={value}", file=sys.stderr)
    if action == "F":
        movement = vec_scale(waypoint, value)
        position = vec_sum(position, movement)
    elif action in {"L", "R"}:
        steps = int(value / 90)
        for _ in range(steps):
            waypoint = vec_rotate(waypoint, action)
    else:
        waypoint, _ = apply_action(waypoint, 0, action, value)

print(f"PART II: Final position: {position}", file=sys.stderr)
distance = abs(position[0]) + abs(position[1])
print(f"PART II: Manhattan distance: {distance}")
