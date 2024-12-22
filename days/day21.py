from typing import Iterable

from .day import Day
from collections import namedtuple, deque
from abc import ABC


Pos = namedtuple('Pos', 'row col')
UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
ACTIVATE = 'A'


class Keypad(ABC):
    def __init__(self):
        self.keys: dict[Pos, str] = {}
        self.pos = Pos(0, 0)

    def dpad_sequence(self, keys: str) -> str:
        """
        Returns one of the dpad sequences that would cause `keys` to be pressed by a robot
        """
        ret = []
        for key in keys:
            target = self._find_pos(key)
            while self.pos != target:
                if self.pos.row != target.row:
                    if target.row > self.pos.row:
                        ret.append(DOWN)
                        self.pos = Pos(self.pos.row+1, self.pos.col)
                    else:
                        ret.append(UP)
                        self.pos = Pos(self.pos.row-1, self.pos.col)
                else:
                    if target.col > self.pos.col:
                        ret.append(RIGHT)
                        self.pos = Pos(self.pos.row, self.pos.col+1)
                    else:
                        ret.append(LEFT)
                        self.pos = Pos(self.pos.row, self.pos.col-1)
            ret.append(ACTIVATE)
        return ''.join(ret)

    def move_and_push(self, key: str) -> Iterable[tuple[str, ...]]:
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
                yield steps + (ACTIVATE,)
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
                elif target.col != pos.col:
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
        self.num_robot = NumericKeypad()
        self.dir_robot2 = DirectionalKeypad()
        self.dir_robot1 = DirectionalKeypad()
        self.me = DirectionalKeypad()

    def shortest(self, code) -> int:
        print(f"{code=}")
        seq1 = self.num_robot.dpad_sequence(code)
        print(f"{seq1=}")
        seq2 = self.dir_robot2.dpad_sequence(seq1)
        print(f"{seq2=}")
        seq3 = self.dir_robot1.dpad_sequence(seq2)
        print(f"{seq3=}")
        return len(seq3)

    def part1(self) -> str:
        answer = 0
        for code in self.data_lines():
            dist = self.shortest(code)
            mult = int(''.join(c for c in code if c.isnumeric()))
            print(f"{code=}, {dist=}, {mult=}, {dist*mult=}")
            answer += dist * mult
        return str(answer)

    def part2(self) -> str:
        return "dayXX 2"
