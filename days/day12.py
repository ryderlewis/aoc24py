from .day import Day
from collections import namedtuple


Pos = namedtuple('Pos', 'row col')


class Day12(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid = self.parse()
        price = 0
        while grid:
            positions, _, perim = self.get_region(grid)
            price += len(positions) * perim
        return str(price)

    def part2(self) -> str:
        grid = self.parse()
        price = 0
        while grid:
            positions, _, _ = self.get_region(grid)
            price += len(positions) * self.sides(positions)
        return str(price)

    @staticmethod
    def sides(grid: set[Pos]) -> int:
        to_check = set()
        count = 0

        for p in grid:
            for d in 'udlr':
                to_check.add((p, d))

        while to_check:
            pos, direction = to_check.pop()
            if direction == 'u':
                # check the top side
                check, prev, next = Pos(-1, 0), Pos(0, -1), Pos(0, 1)
            elif direction == 'd':
                # check the bottom side
                check, prev, next = Pos(1, 0), Pos(0, -1), Pos(0, 1)
            elif direction == 'l':
                # check the left side
                check, prev, next = Pos(0, -1), Pos(1, 0), Pos(-1, 0)
            else:
                # direction == 'r'
                # check the left side
                check, prev, next = Pos(0, 1), Pos(-1, 0), Pos(1, 0)

            if Pos(pos.row+check.row, pos.col+check.col) in grid:
                # not an edge
                continue

            # if here, this is an edge
            count += 1

            # discard any other edges in this line from to_check
            ppos = Pos(pos.row+prev.row, pos.col+prev.col)
            while ppos in grid:
                if Pos(ppos.row+check.row, ppos.col+check.col) in grid:
                    # not an edge
                    break
                else:
                    # also an edge
                    to_check.discard((ppos, direction))
                ppos = Pos(ppos.row+prev.row, ppos.col+prev.col)

            # discard any other edges in this line from to_check
            npos = Pos(pos.row+next.row, pos.col+next.col)
            while npos in grid:
                if Pos(npos.row+check.row, npos.col+check.col) in grid:
                    # not an edge
                    break
                else:
                    # also an edge
                    to_check.discard((npos, direction))
                npos = Pos(npos.row+next.row, npos.col+next.col)

        return count

    @staticmethod
    def get_region(grid: dict[Pos, str]) -> tuple[set[Pos], str, int]:
        pos, char = list(grid.items())[0]
        region = {pos}
        work = [pos]
        perimeter = 0
        while work:
            pos = work.pop()
            for d in [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]:
                npos = Pos(pos.row+d.row, pos.col+d.col)
                if grid.get(npos, None) == char:
                    if npos not in region:
                        region.add(npos)
                        work.append(npos)
                else:
                    perimeter += 1
        for pos in region:
            grid.pop(pos)
        return region, char, perimeter

    def parse(self) -> dict[Pos, str]:
        ret = {}
        for row, line in enumerate(self.data_lines()):
            for col, c in enumerate(line):
                ret[Pos(row, col)] = c
        return ret
