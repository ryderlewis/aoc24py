from .day import Day
from collections import Counter


class Day01(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        nums = [list(map(int, line.split())) for line in self.data_lines()]
        l1 = sorted([x[0] for x in nums])
        l2 = sorted([x[1] for x in nums])
        dist = 0
        for i1, i2 in zip(l1, l2):
            dist += abs(i2-i1)
        return str(dist)


    def part2(self) -> str:
        nums = [list(map(int, line.split())) for line in self.data_lines()]
        l1 = [x[0] for x in nums]
        l2 = Counter([x[1] for x in nums])
        sim = 0
        for i in l1:
            sim += i * l2[i]
        return str(sim)

