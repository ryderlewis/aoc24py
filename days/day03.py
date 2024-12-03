from .day import Day
import re


class Day03(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = 0
        for m in self.muls():
            v1, v2 = map(int, m[4:].rstrip(')').split(','))
            s += v1*v2
        return str(s)

    def part2(self) -> str:
        s = 0
        for m in self.muls2():
            v1, v2 = map(int, m[4:].rstrip(')').split(','))
            s += v1*v2
        return str(s)

    def muls(self) -> list[str]:
        ret = []
        for line in self.data_lines():
            for m in re.finditer(r'mul\(\d+,\d+\)', line):
                ret.append(m.group(0))
        return ret

    def muls2(self) -> list[str]:
        ret = []
        do = True
        for line in self.data_lines():
            for m in re.finditer(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', line):
                g = m.group(0)
                if g == 'do()':
                    do = True
                elif g == "don't()":
                    do = False
                elif g.startswith('mul'):
                    if do:
                        ret.append(g)
        return ret
