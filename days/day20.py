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

                # find all points that are within max_dist manhattan distance of start_pos
                # and for any of them that are on the path, yield the new total distance
                for end_pos, manhattan_dist in self.manhattan_points(start_pos, max_dist):
                    cheat_dist = self.start_dists[start_pos] + self.end_dists[end_pos] + manhattan_dist
                    yield start_pos, end_pos, cheat_dist

    def manhattan_points(self, start_pos: Pos, max_dist: int) -> Iterable[tuple[Pos, int]]:
        for dr in range(-max_dist, max_dist+1):
            for dc in range(-max_dist+abs(dr), max_dist+1-abs(dr)):
                if dr == 0 and dc == 0:
                    continue
                end_pos = Pos(start_pos.row+dr, start_pos.col+dc)
                if end_pos in self.end_dists:
                    yield end_pos, abs(dr)+abs(dc)

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
