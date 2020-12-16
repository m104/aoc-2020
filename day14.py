#!/usr/bin/env python3
#
# Debug:
#   ./day14.py < day14.input.txt
# Run:
#   ./day14.py < day14.input.txt 2>/dev/null

import re
import sys

from collections import defaultdict


input_lines = []
for line in sys.stdin:
    input_lines.append(line.strip())


def extract_matching_bits(bit_value, mask):
    enumerated_mask = enumerate(reversed(mask))
    matching = filter(lambda t: t[1] == bit_value, enumerated_mask)
    return set(map(lambda t: t[0], matching))


def build_or_mask(bits):
    mask = 0
    for bit in bits:
        mask += 2 ** bit
    return mask


def build_and_mask(bits):
    mask = (2 ** 36) - 1
    for bit in bits:
        mask -= 2 ** bit
    return mask


def build_floating_addresses(addresses, floating_bits):
    bit = list(floating_bits)[0]
    new_addresses = [address + (2 ** bit) for address in addresses]
    remaining_bits = floating_bits - {bit}
    if remaining_bits:
        return build_floating_addresses(addresses + new_addresses, remaining_bits)
    else:
        return addresses + new_addresses


class Operation:
    def __init__(self, mask, writes):
        self.mask = mask
        self.and_mask = build_and_mask(extract_matching_bits("0", mask))
        self.or_mask = build_or_mask(extract_matching_bits("1", mask))
        self.floating_bits = extract_matching_bits("X", mask)
        self.floating_mask = build_and_mask((self.floating_bits))
        self.writes = writes

    def __repr__(self):
        return f"Operation(mask={self.mask!r}, writes={self.writes!r})"

    def masked_value(self, value):
        result = value & self.and_mask | self.or_mask
        print(f"mask_value({value}):", file=sys.stderr)
        print(f"     value: {bin(value)[2:]:>36}", file=sys.stderr)
        print(f"      mask: {self.mask:>36}", file=sys.stderr)
        print(f"  and_mask: {bin(self.and_mask)[2:]:>36}", file=sys.stderr)
        print(f"   or_mask: {bin(self.or_mask)[2:]:>36}", file=sys.stderr)
        print(f"    result: {bin(result)[2:]:>36}", file=sys.stderr)
        return result

    def masked_writes(self):
        return [(address, self.masked_value(value)) for address, value in self.writes]

    def floating_writes(self):
        print("floating_writes(0):", file=sys.stderr)
        writes = []
        print(f"     mask: {self.mask:>36}", file=sys.stderr)
        print(f" and_mask: {bin(self.floating_mask)[2:]:>36} ({self.floating_mask})", file=sys.stderr)
        print(f"  or_mask: {bin(self.or_mask)[2:]:>36} ({self.or_mask})", file=sys.stderr)
        for base_address, value in self.writes:
            masked_address = base_address & self.floating_mask | self.or_mask
            all_addresses = build_floating_addresses([masked_address], self.floating_bits)
            print(f"  address: {bin(masked_address)[2:]:>36} ({masked_address})", file=sys.stderr)
            for address in all_addresses:
                print(f"  >masked: {bin(address)[2:]:>36} ({address})", file=sys.stderr)
            writes += [(address, value) for address in sorted(all_addresses)]
        return writes


def group_operations(input_lines):
    mask_pattern = re.compile(r"^mask = (?P<mask>[01X]{36})$")
    write_pattern = re.compile(r"^mem\[(?P<address>\d+)\] = (?P<value>\d+)")

    operations = []
    mask = None
    writes = []

    for line in input_lines:
        match = mask_pattern.fullmatch(line)
        if match:
            if mask and writes:
                operations.append(Operation(mask, writes))
                print(f"Adding mask={mask} writes={writes}", file=sys.stderr)
            mask = match.groups()[0]
            writes = []
            continue

        match = write_pattern.fullmatch(line)
        if match:
            address, value = match.groups()
            writes.append((int(address), int(value)))
            continue

        print(f"line={line!r}", file=sys.stderr)
        raise ValueError("No matching input pattern found!")

    if mask and writes:
        operations.append(Operation(mask, writes))
        print(f"Adding mask={mask} writes={writes}", file=sys.stderr)

    return operations


operations = group_operations(input_lines)
memory = defaultdict(int)

for operation in operations:
    for address, value in operation.masked_writes():
        print(f"Writing mem[{address}] = {value}", file=sys.stderr)
        memory[address] = value

answer = sum(memory.values())
print(f"Part I Answer: {answer}")

memory = defaultdict(int)

for operation in operations:
    for address, value in operation.floating_writes():
        print(f"Writing mem[{address}] = {value}", file=sys.stderr)
        memory[address] = value

answer = sum(memory.values())
print(f"Part II Answer: {answer}")
