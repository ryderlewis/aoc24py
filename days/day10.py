from .day import Day
from collections import deque, namedtuple


Pos = namedtuple('Pos', 'row col')


class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def score(grid: list[list[int]], trailhead: Pos) -> int:
        work = deque([(trailhead, 0)])
        seen = {trailhead}
        score = 0
        while work:
            pos, elevation = work.popleft()
            if elevation == 9:
                score += 1
                continue
            for direction in (Pos(-1, 0), Pos(1, 0), Pos(0, 1), Pos(0, -1)):
                test_pos = Pos(pos.row+direction.row, pos.col+direction.col)
                if test_pos in seen:
                    continue
                if 0 <= test_pos.row < len(grid) and 0 <= test_pos.col < len(grid[0]) and grid[test_pos.row][test_pos.col] == elevation + 1:
                    seen.add(test_pos)
                    work.append((test_pos, elevation + 1))
        return score

    def part1(self) -> str:
        grid = self.parse()
        score = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 0:
                    score += self.score(grid, Pos(row, col))
        return str(score)

    @staticmethod
    def rating(grid: list[list[int]], trailhead: Pos) -> int:
        work: deque[tuple[tuple[Pos, ...], int]] = deque([((trailhead,), 0)])
        seen: set[tuple[Pos, ...]] = {(trailhead,)}
        score = 0
        while work:
            trail, elevation = work.popleft()
            if elevation == 9:
                score += 1
                continue
            pos = trail[-1]
            for direction in (Pos(-1, 0), Pos(1, 0), Pos(0, 1), Pos(0, -1)):
                test_pos = Pos(pos.row+direction.row, pos.col+direction.col)
                test_trail: tuple[Pos, ...] = trail + (test_pos,)
                if test_trail in seen:
                    continue
                if 0 <= test_pos.row < len(grid) and 0 <= test_pos.col < len(grid[0]) and grid[test_pos.row][test_pos.col] == elevation + 1:
                    seen.add(test_trail)
                    work.append((test_trail, elevation + 1))
        return score

    def part2(self) -> str:
        grid = self.parse()
        score = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 0:
                    score += self.rating(grid, Pos(row, col))
        return str(score)

    def parse(self) -> list[list[int]]:
        return [list(map(int, line)) for line in self.data_lines()]
