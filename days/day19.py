from .day import Day
from functools import lru_cache


class Day19(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towels, self.patterns = self.parse()

    @lru_cache(maxsize=None)
    def possible(self, pattern: str) -> int:
        if pattern == "":
            return 1
        count = 0
        for t in self.towels:
            if pattern.startswith(t):
                count += self.possible(pattern[len(t):])
        return count

    def part1(self) -> str:
        return str(sum(1 for p in self.patterns if self.possible(p)))

    def part2(self) -> str:
        return str(sum(self.possible(p) for p in self.patterns))

    def parse(self) -> tuple[set[str], list[str]]:
        towels, patterns = set(), []
        for i, line in enumerate(self.data_lines()):
            if i == 0:
                towels = {s.strip() for s in line.split(',')}
            elif i != 1:
                patterns.append(line)
        return towels, patterns
