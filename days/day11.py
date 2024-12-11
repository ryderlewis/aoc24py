from typing import Iterable
from functools import lru_cache
import math

from .day import Day


class Day11(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: dict[int, tuple[int, int]] = {}

    @lru_cache(maxsize=None)
    def count_next(self, val: int, remaining: int) -> int:
        if remaining == 0:
            return 1

        if val == 0:
            return self.count_next(1, remaining - 1)
        elif math.floor(math.log10(val)) % 2 == 1:
            if val not in self._seen:
                d = str(val)
                self._seen[val] = (int(d[:len(d)//2]), int(d[len(d)//2:]))
            n1, n2 = self._seen[val]
            return self.count_next(n1, remaining - 1) + self.count_next(n2, remaining - 1)
        else:
            return self.count_next(val * 2024, remaining - 1)

    def part1(self) -> str:
        stones = list(map(int, self.data_lines()[0].split()))
        return str(sum(self.count_next(v, 25) for v in stones))

    def part2(self) -> str:
        stones = list(map(int, self.data_lines()[0].split()))
        return str(sum(self.count_next(v, 75) for v in stones))
