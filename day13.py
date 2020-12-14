#!/usr/bin/env python3
#
# Debug:
#   ./day13.py < day13.input.txt
# Run:
#   ./day13.py < day13.input.txt 2>/dev/null

import math
import sys


input_lines = []
for line in sys.stdin:
    input_lines.append(line.strip())


def print_schedule(when, active_lines, window=30):
    print(f"when={when} active_lines={active_lines}", file=sys.stderr)
    
    legend = "   "
    for line in active_lines:
        legend += "%4s " % line
    legend += "  time"
    print(legend, file=sys.stderr)

    for time in range(when - 5, when + window):
        if time == when:
            delim = "X"
        else:
            delim = " "

        schedule = ""
        for line in active_lines:
            if (time % line) == 0:
                schedule += "    D"
            else:
                schedule += "    "

        print(f"{delim} {schedule}   {time}", file=sys.stderr)


now = int(input_lines[0])
active_lines = list(map(int, filter(lambda l: l != "x", input_lines[1].split(","))))
print_schedule(now, sorted(active_lines))


def time_until_departure(when, frequency):
    return (frequency - (when % frequency)) % frequency


def parse_schedule(input_line):
    return list(
        map(
            lambda t: (t[0], int(t[1])),
            filter(lambda t: t[1] != "x", enumerate(input_line.split(","))),
        )
    )


def next_schedule_target(timestamp, run, frequency, target):
    target = target % frequency
    while True:
        offset = time_until_departure(timestamp, frequency)
        print(
            f"run={run} frequency={frequency} timestamp={timestamp} target={target} offset={offset}",
            file=sys.stderr,
        )
        if offset == target:
            break
        timestamp += run
    return timestamp


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def calculate_soonest_departure(schedule):
    timestamp = schedule[0][1]
    run = timestamp
    for target, frequency in schedule[1:]:
        print(f"frequency={frequency} target={target}", file=sys.stderr)
        timestamp = next_schedule_target(timestamp, run, frequency, target)
        run = lcm(run, frequency)
    return timestamp


departures = map(lambda l: (time_until_departure(now, l), l), active_lines)
best_line, wait_time = sorted(departures)[0]
print(f"best departure: line={best_line} wait_time={wait_time}", file=sys.stderr)
answer = best_line * wait_time
print(f"Part I answer: {answer}")

# test_input = "7,13,x,x,59,x,31,19"
# schedule = parse_schedule(test_input)
# active_lines = list(map(int, filter(lambda l: l != "x", test_input.split(","))))

schedule = parse_schedule(input_lines[1])
print(f"schedule={schedule}", file=sys.stderr)

answer = calculate_soonest_departure(schedule)
print_schedule(answer, active_lines)
print(f"Part II answer: {answer}")
