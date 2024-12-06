from .day import Day


DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Day06(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid, pos = self.parse()
        rows, cols = len(grid), len(grid[0])
        seen = {pos}
        d = 0
        while True:
            seen.add(pos)
            next_pos = (pos[0] + DIRS[d][0], pos[1] + DIRS[d][1])
            if next_pos[0] < 0 or next_pos[0] >= rows or next_pos[1] < 0 or next_pos[1] >= cols:
                return str(len(seen))
            if grid[next_pos[0]][next_pos[1]] == '#':
                d += 1
                d %= len(DIRS)
            else:
                pos = next_pos

    def part2(self) -> str:
        grid, pos = self.parse()
        count = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == '.':
                    grid[row][col] = '#'
                    if self.loops(grid, pos):
                        count += 1
                    grid[row][col] = '.'
        return str(count)

    def loops(self, grid: list[list[str]], pos: tuple[int, int]) -> bool:
        rows, cols = len(grid), len(grid[0])
        d = 0
        seen = set()
        while True:
            if (pos, d) in seen:
                return True
            seen.add((pos, d))
            next_pos = (pos[0] + DIRS[d][0], pos[1] + DIRS[d][1])
            if next_pos[0] < 0 or next_pos[0] >= rows or next_pos[1] < 0 or next_pos[1] >= cols:
                return False
            if grid[next_pos[0]][next_pos[1]] == '#':
                d += 1
                d %= len(DIRS)
            else:
                pos = next_pos

    def parse(self) -> tuple[list[list[str]], tuple[int, int]]:
        grid = [list(line) for line in self.data_lines()]
        for r, row in enumerate(grid):
            if '^' in row:
                return grid, (r, row.index('^'))
