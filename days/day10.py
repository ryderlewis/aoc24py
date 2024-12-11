from .day import Day
from collections import deque, namedtuple


Pos = namedtuple('Pos', 'row col')


class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def score(grid: list[list[int]], trailhead: Pos) -> tuple[int, int]:
        work: deque[tuple[tuple[Pos, ...], int]] = deque([((trailhead,), 0)])
        seen: set[tuple[Pos, ...]] = {(trailhead,)}
        unique_ends = set()
        rating = 0
        while work:
            trail, elevation = work.popleft()
            pos = trail[-1]
            if elevation == 9:
                rating += 1
                unique_ends.add(pos)
                continue
            for direction in (Pos(-1, 0), Pos(1, 0), Pos(0, 1), Pos(0, -1)):
                test_pos = Pos(pos.row+direction.row, pos.col+direction.col)
                test_trail: tuple[Pos, ...] = trail + (test_pos,)
                if test_trail in seen:
                    continue
                if 0 <= test_pos.row < len(grid) and 0 <= test_pos.col < len(grid[0]) and grid[test_pos.row][test_pos.col] == elevation + 1:
                    seen.add(test_trail)
                    work.append((test_trail, elevation + 1))
        return len(unique_ends), rating

    def score_and_rating(self) -> tuple[int, int]:
        grid = self.parse()
        score = 0
        rating = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 0:
                    s, r = self.score(grid, Pos(row, col))
                    score += s
                    rating += r
        return score, rating

    def part1(self) -> str:
        return str(self.score_and_rating()[0])

    def part2(self) -> str:
        return str(self.score_and_rating()[1])

    def parse(self) -> list[list[int]]:
        return [list(map(int, line)) for line in self.data_lines()]
