#!/usr/bin/env python3
from days import factory
import sys

if __name__ == '__main__':
    sys. setrecursionlimit(1_000)
    if len(sys.argv) < 4:
        raise Exception("Must provide arguments for the day, part, and filename")
    day = int(sys.argv[1])
    part = int(sys.argv[2])
    filename = sys.argv[3]
    if day < 1 or day > 25:
        raise Exception("Day must be between 1 and 25, inclusive")
    if part not in (1, 2):
        raise Exception("Part must be 1 or 2")

    print(factory(filename=filename, day=day, part=part).run())
