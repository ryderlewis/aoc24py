from .day import Day
from collections import namedtuple
import heapq

Pos = namedtuple('Pos', 'row col')
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SOUTH, EAST, NORTH, WEST = 0, 1, 2, 3


class Day16(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _find_start(self, grid: tuple[tuple[str, ...], ...]) -> Pos:
        for row, squares in enumerate(grid):
            for col, square in enumerate(squares):
                if square == 'S':
                    return Pos(row, col)
        raise RuntimeError("Did not find start")

    def part1(self) -> str:
        maze = self.parse()
        pos = self._find_start(maze)
        work = [(0, pos, EAST)]
        seen = {(pos, EAST)}
        while work:
            score, pos, direction = heapq.heappop(work)
            if maze[pos.row][pos.col] == 'E':
                return str(score)

            # try going straight
            npos = Pos(pos.row + DIRS[direction][0], pos.col + DIRS[direction][1])
            if (npos, direction) not in seen:
                if maze[npos.row][npos.col] != '#':
                    seen.add((npos, direction))
                    heapq.heappush(work, (score + 1, npos, direction))

            # and turn left/right
            for delta in (-1, 1):
                d = (direction + delta) % len(DIRS)
                if (pos, d) not in seen:
                    seen.add((pos, d))
                    heapq.heappush(work, (score + 1000, pos, d))

        return "dayXX 1"

    def part2(self) -> str:
        return "dayXX 2"

    def parse(self) -> tuple[tuple[str, ...], ...]:
        return tuple([tuple(line) for line in self.data_lines()])