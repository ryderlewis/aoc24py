from .day import Day
from collections import defaultdict


class Day08(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        locs = defaultdict(set)
        grid = self.parse()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (c := grid[row][col]) != '.':
                    locs[c].add((row, col))

        antinodes = set()
        for s in locs.values():
            ss = sorted(s)
            for i in range(len(ss)-1):
                for j in range(i+1, len(ss)):
                    pos1, pos2 = ss[i], ss[j]
                    if pos1[0] > pos2[0]:
                        pos1, pos2 = pos2, pos1
                    dr, dc = pos2[0]-pos1[0], pos2[1]-pos1[1]
                    an1 = (pos1[0]-dr, pos1[1]-dc)
                    an2 = (pos2[0]+dr, pos2[1]+dc)
                    if 0 <= an1[0] < len(grid) and 0 <= an1[1] < len(grid[0]):
                        antinodes.add(an1)
                    if 0 <= an2[0] < len(grid) and 0 <= an2[1] < len(grid[0]):
                        antinodes.add(an2)

        return str(len(antinodes))

    def part2(self) -> str:
        locs = defaultdict(set)
        grid = self.parse()
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (c := grid[row][col]) != '.':
                    locs[c].add((row, col))

        antinodes = set()
        for s in locs.values():
            ss = sorted(s)
            for i in range(len(ss)-1):
                for j in range(i+1, len(ss)):
                    pos1, pos2 = ss[i], ss[j]
                    if pos1[0] > pos2[0]:
                        pos1, pos2 = pos2, pos1
                    dr, dc = pos2[0]-pos1[0], pos2[1]-pos1[1]
                    an1 = pos1
                    while 0 <= an1[0] < len(grid) and 0 <= an1[1] < len(grid[0]):
                        antinodes.add(an1)
                        an1 = (an1[0]-dr, an1[1]-dc)
                    an2 = pos2
                    while 0 <= an2[0] < len(grid) and 0 <= an2[1] < len(grid[0]):
                        antinodes.add(an2)
                        an2 = (an2[0]+dr, an2[1]+dc)

        return str(len(antinodes))

    def parse(self) -> list[list[str]]:
        return [list(line) for line in self.data_lines()]