from .day import Day


class Day04(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid = self.parse()
        cols = len(grid[0])
        rows = len(grid)
        xmas = 0
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 'X':
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            for i, c in zip(range(1, 4), 'MAS'):
                                r2, c2 = row + i * dr, col + i * dc
                                if not (0 <= r2 < rows and 0 <= c2 < cols):
                                    break
                                if grid[r2][c2] != c:
                                    break
                                if c == 'S':
                                    xmas += 1
        return str(xmas)

    def part2(self) -> str:
        grid = self.parse()
        cols = len(grid[0])
        rows = len(grid)
        xmas = 0
        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if grid[row][col] == 'A':
                    d1a, d1b = grid[row-1][col-1], grid[row+1][col+1]
                    d2a, d2b = grid[row-1][col+1], grid[row+1][col-1]
                    if sorted([d1a, d1b]) == ['M', 'S'] and sorted([d2a, d2b]) == ['M', 'S']:
                        xmas += 1
        return str(xmas)

    def parse(self) -> tuple[tuple[str, ...], ...]:
        ret = []
        for line in self.data_lines():
            ret.append(tuple(line))
        return tuple(ret)
