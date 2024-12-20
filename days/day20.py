from typing import Iterable

from .day import Day
from collections import namedtuple, deque, Counter

Pos = namedtuple('Pos', 'row col')


class Maze:
    def __init__(self, lines: list[str]):
        self.grid = tuple(tuple(line) for line in lines)
        self.start, self.end = None, None
        for row, vals in enumerate(self.grid):
            for col, c in enumerate(vals):
                if c == 'S':
                    self.start = Pos(row, col)
                elif c == 'E':
                    self.end = Pos(row, col)
        assert isinstance(self.start, Pos)
        assert isinstance(self.end, Pos)

        self.end_dists = self._find_dists(self.end)
        self.start_dists = self._find_dists(self.start)

    def shortest_without_cheat(self) -> int:
        return self.start_dists[self.end]

    def cheats(self, max_dist: int) -> Iterable[tuple[Pos, Pos, int]]:
        # enumerate all the possible cheats, defined as start_pos/end_pos pairs
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == '#':
                    continue
                start_pos = Pos(row, col)
                for dr, dc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                    wall_pos = Pos(start_pos.row+dr, start_pos.col+dc)
                    if self.grid[wall_pos.row][wall_pos.col] != '#':
                        continue
                    for wr, wc in ((-1, 0), (1, 0), (0, 1), (0, -1)):
                        end_pos = Pos(wall_pos.row+wr, wall_pos.col+wc)
                        if end_pos == start_pos or end_pos not in self.end_dists:
                            continue
                        cheat_dist = self.start_dists[start_pos] + self.end_dists[end_pos] + 2
                        yield start_pos, end_pos, cheat_dist

    def _find_dists(self, pos: Pos) -> dict[Pos, int]:
        work = deque([(0, pos)])
        dists = {pos: 0}
        while work:
            dist, pos = work.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                npos = Pos(pos.row+dr, pos.col+dc)
                if self.grid[npos.row][npos.col] != '#' and npos not in dists:
                    dists[npos] = dist+1
                    work.append((dist+1, npos))
        return dists


class Day20(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maze = Maze(self.data_lines())

    def answer(self, max_dist: int) -> int:
        dist = self.maze.shortest_without_cheat()
        c = Counter()
        for _, _, cdist in self.maze.cheats(max_dist):
            if cdist < dist:
                c.update({dist-cdist: 1})
        return sum(v for k, v in c.items() if k >= 100)

    def part1(self) -> str:
        return str(self.answer(2))

    def part2(self) -> str:
        return str(self.answer(20))
