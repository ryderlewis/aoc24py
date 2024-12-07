from .day import Day
from itertools import permutations, combinations_with_replacement


class Day07(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        ret = 0
        for ans, vals in self.parse():
            if self.can_answer(ans, vals):
                ret += ans
        return str(ret)

    def can_answer(self, ans: int, vals: tuple[int, ...]) -> bool:
        if len(vals) == 1:
            return ans == vals[0]

        if ans % vals[-1] == 0:
            if self.can_answer(ans//vals[-1], vals[:-1]):
                return True

        if self.can_answer(ans-vals[-1], vals[:-1]):
            return True

        return False

    def part2(self) -> str:
        ret = 0
        for ans, vals in self.parse():
            if self.can_answer_2(0, ans, vals):
                ret += ans
        return str(ret)

    def can_answer_2(self, calc: int, ans: int, vals: tuple[int, ...]) -> bool:
        if len(vals) == 0:
            return calc == ans
        elif calc > ans:
            return False

        if self.can_answer_2(calc + vals[0], ans, vals[1:]):
            return True

        # concat and mult can only happen after the first term (when calc > 0)
        if calc > 0:
            if self.can_answer_2(int(f"{calc}{vals[0]}"), ans, vals[1:]):
                return True
            if self.can_answer_2(calc * vals[0], ans, vals[1:]):
                return True

        return False

    def parse(self) -> list[tuple[int, tuple[int, ...]]]:
        ret = []
        for line in self.data_lines():
            res, vals = line.split(': ')
            ret.append((int(res), tuple(map(int, vals.split()))))
        return ret
