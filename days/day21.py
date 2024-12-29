from typing import Iterable

from .day import Day
from collections import namedtuple, deque
from abc import ABC
from functools import lru_cache


Pos = namedtuple('Pos', 'row col')
UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
ACTIVATE = 'A'


class Keypad(ABC):
    def __init__(self):
        self.keys: dict[Pos, str] = {}
        self.pos = Pos(0, 0)

    def dpad_sequences(self, key: str) -> Iterable[str]:
        """
        moves current position to the given key, and returns
        an iterable of the various direction options to get there followed by
        the push action
        """
        target = self._find_pos(key)
        # this is probably an inefficient way to find all the permutations
        # of directions to go, but meh
        work: deque[tuple[Pos, tuple[str, ...]]] = deque([(self.pos, ())])
        self.pos = target

        while work:
            pos, steps = work.popleft()

            if pos == target:
                seq = ''.join(steps + (ACTIVATE,))
                yield seq
            else:
                if target.row != pos.row:
                    if target.row < pos.row:
                        npos = Pos(pos.row-1, pos.col)
                        step = UP
                    else:
                        npos = Pos(pos.row+1, pos.col)
                        step = DOWN
                    if npos in self.keys:
                        work.append((npos, steps + (step,)))
                if target.col != pos.col:
                    if target.col < pos.col:
                        npos = Pos(pos.row, pos.col-1)
                        step = LEFT
                    else:
                        npos = Pos(pos.row, pos.col+1)
                        step = RIGHT
                    if npos in self.keys:
                        work.append((npos, steps + (step,)))

    def _find_pos(self, key: str) -> Pos:
        for pos, k in self.keys.items():
            if k == key:
                return pos
        raise ValueError(key)


class NumericKeypad(Keypad):
    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    """
    def __init__(self):
        super().__init__()
        self.keys = {
            Pos(0, 0): '7',
            Pos(0, 1): '8',
            Pos(0, 2): '9',
            Pos(1, 0): '4',
            Pos(1, 1): '5',
            Pos(1, 2): '6',
            Pos(2, 0): '1',
            Pos(2, 1): '2',
            Pos(2, 2): '3',
            Pos(3, 1): '0',
            Pos(3, 2): 'A',
        }
        self.pos = Pos(3, 2)


class DirectionalKeypad(Keypad):
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    def __init__(self):
        super().__init__()
        self.keys = {
            Pos(0, 1): UP,
            Pos(0, 2): 'A',
            Pos(1, 0): LEFT,
            Pos(1, 1): DOWN,
            Pos(1, 2): RIGHT,
        }
        self.pos = Pos(0, 2)

class Day21(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @lru_cache(maxsize=None)
    def shortest(self, code: str, pressers: tuple[Keypad, ...]) -> int:
        presser, pressers = pressers[0], pressers[1:]
        if len(pressers) == 0:
            return len(code)

        dist = 0
        for key in code:
            best = None
            for seq in presser.dpad_sequences(key):
                count = self.shortest(seq, pressers)
                if best is None:
                    best = count
                else:
                    best = min(best, count)
            dist += best
        return dist

    def answer(self, num_dpad_robots: int) -> int:
        answer = 0
        pressers = [NumericKeypad()] + [DirectionalKeypad() for _ in range(num_dpad_robots + 1)]
        for code in self.data_lines():
            dist = self.shortest(code, tuple(pressers))
            mult = int(''.join(c for c in code if c.isnumeric()))
            answer += dist * mult
        return answer

    def part1(self) -> str:
        return str(self.answer(2))

    def part2(self) -> str:
        return str(self.answer(25))
