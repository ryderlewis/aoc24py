from .day import Day
from collections import namedtuple
import re


Vec = namedtuple('Vec', 'x y')


class ClawMachine:
    def __init__(self, a_button: Vec, b_button: Vec, prize: Vec):
        self.a_button = a_button
        self.b_button = b_button
        self.prize = prize

    def presses(self) -> tuple[int, int] | None:
        """
        Returns a tuple of (a, b) button presses, or None

        The calculation is a system of linear equations:

        a_button.x*A + b_button.x*B = Vec.x
        a_button.y*A + b_button.y*B = Vec.y

        ax(A) + bx(B) = vx
        ay(A) + by(B) = vy
        solve for A and B.

        C1x + C2y = C3
        C4x + C5y = C6

        easiest solution:
        multiply terms on top equation by C4
        multiply terms on bottom equation by C1

        C4*C1x + C4*C2y = C4*C3
        C1*C4x + C!*C5y = C1*C6

        (C4*C2 - C1*C5)y = C4*C3-C1*C6

        y = (C4*C3-C1*C6) / (C4*C2 - C1*C5)  => if this is a non-negative integer
        C1x + C2y = C3
        x = (c3 - C2y) / C1   => if this is a non-negative integer
        """
        c1 = self.a_button.x
        c2 = self.b_button.x
        c3 = self.prize.x
        c4 = self.a_button.y
        c5 = self.b_button.y
        c6 = self.prize.y

        numerator = c4*c3 - c1*c6
        denominator = c4*c2 - c1*c5
        if denominator == 0 or numerator % denominator != 0:
            return None
        y = numerator // denominator
        if y < 0:
            return None
        b_count = y

        numerator = c3 - c2 * y
        denominator = c1
        if denominator == 0 or numerator % denominator != 0:
            return None
        x = numerator // denominator
        if x < 0:
            return None
        a_count = x

        return a_count, b_count


class Day13(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        machines = self.parse()
        cost = 0
        for m in machines:
            if (p := m.presses()) is not None:
                a, b = p
                cost += 3*a + b
        return str(cost)

    def part2(self) -> str:
        delta = 10000000000000
        machines = self.parse()
        cost = 0
        for m in machines:
            m.prize = Vec(m.prize.x + delta, m.prize.y + delta)
            if (p := m.presses()) is not None:
                a, b = p
                cost += 3*a + b
        return str(cost)

    def parse(self) -> list[ClawMachine]:
        ret = []
        for line in self.data_lines():
            """
            Button A: X+54, Y+22
            Button B: X+36, Y+62
            Prize: X=19754, Y=14184
            """
            if (m := re.match(r'Button A: X\+(\d+), Y\+(\d+)', line)) is not None:
                x, y = map(int, m.groups())
                button_a = Vec(x, y)
            elif (m := re.match(r'Button B: X\+(\d+), Y\+(\d+)', line)) is not None:
                x, y = map(int, m.groups())
                button_b = Vec(x, y)
            elif (m := re.match(r'Prize: X=(\d+), Y=(\d+)', line)) is not None:
                x, y = map(int, m.groups())
                prize = Vec(x, y)
                ret.append(ClawMachine(button_a, button_b, prize))
        return ret

if __name__ == '__main__':
    m = ClawMachine(Vec(94, 34), Vec(22, 67), Vec(8400, 5400))
    a, b = m.presses()
    print(f"{a=}, {b=}")
