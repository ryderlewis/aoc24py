from .day import Day
from .day01 import Day01
from .day02 import Day02
from .day03 import Day03
from .day04 import Day04
from .day05 import Day05
from .day06 import Day06
from .day07 import Day07
from .day08 import Day08
from .day09 import Day09
from .day10 import Day10
from .day11 import Day11
from .day12 import Day12
from .day13 import Day13
from .day14 import Day14
from .day15 import Day15
from .day16 import Day16
from .day17 import Day17
from .day18 import Day18
from .day19 import Day19
from .day20 import Day20
from .day21 import Day21
from .day22 import Day22
from .day23 import Day23
from .day24 import Day24
from .day25 import Day25


def factory(*, filename: str, day: int, part: int) -> Day:
    kwargs = {
        'filename': filename,
        'part': part,
    }

    if day == 1:
        return Day01(**kwargs)
    elif day == 2:
        return Day02(**kwargs)
    elif day == 3:
        return Day03(**kwargs)
    elif day == 4:
        return Day04(**kwargs)
    elif day == 5:
        return Day05(**kwargs)
    elif day == 6:
        return Day06(**kwargs)
    elif day == 7:
        return Day07(**kwargs)
    elif day == 8:
        return Day08(**kwargs)
    elif day == 9:
        return Day09(**kwargs)
    elif day == 10:
        return Day10(**kwargs)
    elif day == 11:
        return Day11(**kwargs)
    elif day == 12:
        return Day12(**kwargs)
    elif day == 13:
        return Day13(**kwargs)
    elif day == 14:
        return Day14(**kwargs)
    elif day == 15:
        return Day15(**kwargs)
    elif day == 16:
        return Day16(**kwargs)
    elif day == 17:
        return Day17(**kwargs)
    elif day == 18:
        return Day18(**kwargs)
    elif day == 19:
        return Day19(**kwargs)
    elif day == 20:
        return Day20(**kwargs)
    elif day == 21:
        return Day21(**kwargs)
    elif day == 22:
        return Day22(**kwargs)
    elif day == 23:
        return Day23(**kwargs)
    elif day == 24:
        return Day24(**kwargs)
    elif day == 25:
        return Day25(**kwargs)
    else:
        return Day(**kwargs)
