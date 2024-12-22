from .day import Day
from collections import namedtuple
import heapq
import random

Pos = namedtuple('Pos', 'row col')
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SOUTH, EAST, NORTH, WEST = 0, 1, 2, 3


class Day16(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _find_start(grid: tuple[tuple[str, ...], ...]) -> Pos:
        for row, squares in enumerate(grid):
            for col, square in enumerate(squares):
                if square == 'S':
                    return Pos(row, col)
        raise RuntimeError("Did not find start")

    def shortest(
            self,
            maze: tuple[tuple[str, ...], ...],
    ) -> tuple[int, set[Pos]]:
        pos = self._find_start(maze)
        work = [(0, pos, EAST, {pos})]
        seen = {(pos, EAST): 0}
        best_score = 0
        while work:
            score, pos, direction, all_positions = heapq.heappop(work)
            if maze[pos.row][pos.col] == 'E':
                if best_score == 0:
                    best_score = score
                return score, all_positions

            deltas = [-1, 0, 1]
            random.shuffle(deltas)

            for delta in deltas:
                if delta == 0:
                    # try going straight
                    npos = Pos(pos.row + DIRS[direction][0], pos.col + DIRS[direction][1])
                    if (npos, direction) not in seen or seen[(npos, direction)] > score+1:
                        if maze[npos.row][npos.col] != '#':
                            seen[(npos, direction)] = score+1
                            heapq.heappush(work, (score + 1, npos, direction, all_positions|{npos}))
                else:
                    # and turn left/right
                    d = (direction + delta) % len(DIRS)
                    if (pos, d) not in seen or seen[(pos, d)] > score+1000:
                        seen[(pos, d)] = score + 1000
                        heapq.heappush(work, (score + 1000, pos, d, all_positions))

    def part1(self) -> str:
        return str(self.shortest(self.parse())[0])

    def part2(self) -> str:
        maze = self.parse()
        dist, points = self.shortest(maze)
        for i in range(1, 1001):
            print(f"After {i}, {len(points)=}")
            _, p = self.shortest(maze)
            points.update(p)
        return str(len(p))

    def parse(self) -> tuple[tuple[str, ...], ...]:
        return tuple([tuple(line) for line in self.data_lines()])