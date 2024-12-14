from .day import Day
from collections import namedtuple
from dataclasses import dataclass
import re


Pos = namedtuple('Pos', 'x y')
Vel = namedtuple('Vel', 'dx dy')

@dataclass
class Robot:
    pos: Pos
    vel: Vel

class Day14(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        robots = self.parse()
        width = 101
        height = 103

        ends = []
        for r in robots:
            x = (r.pos.x + r.vel.dx * 100) % width
            y = (r.pos.y + r.vel.dy * 100) % height
            ends.append(Pos(x, y))

        q1, q2, q3, q4 = 0, 0, 0, 0
        for e in ends:
            if e.x < width//2:
                if e.y < height//2:
                    q1 += 1
                if height//2 < e.y:
                    q3 += 1
            if width//2 < e.x:
                if e.y < height//2:
                    q2 += 1
                if height//2 < e.y:
                    q4 += 1

        return str(q1*q2*q3*q4)

    def part2(self) -> str:
        robots = self.parse()
        width = 101
        height = 103

        for i in range(1, 1000001):
            positions = set()
            for r in robots:
                x = (r.pos.x + r.vel.dx) % width
                y = (r.pos.y + r.vel.dy) % height
                r.pos = Pos(x, y)
                positions.add(r.pos)

            if i % 103 == 72:
                print()
                print(f"Step {i}")
                for y in range(height):
                    for x in range(width):
                        if Pos(x, y) in positions:
                            print('#', end='')
                        else:
                            print(' ', end='')
                    print()
        return "dayXX 2"

    def parse(self) -> list[Robot]:
        ret = []
        for line in self.data_lines():
            m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
            px, py, vx, vy = map(int, m.groups())
            ret.append(Robot(Pos(px, py), Vel(vx, vy)))
        return ret
