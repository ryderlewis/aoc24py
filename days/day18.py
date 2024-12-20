from .day import Day
from collections import namedtuple, deque

Pos = namedtuple('Pos', 'x y')


class Day18(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def solve(grid: list[list[str]]) -> int:
        pos = Pos(0, 0)
        end = Pos(70, 70)
        work = deque([(0, pos)])
        seen = {pos}
        while work:
            dist, pos = work.popleft()
            if pos == end:
                return dist
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                npos = Pos(pos.x + dx, pos.y + dy)
                if npos not in seen and 0 <= npos.x <= 70 and 0 <= npos.y <= 70 and grid[npos.y][npos.x] != '#':
                    seen.add(npos)
                    work.append((dist+1, npos))
        return -1

    def part1(self) -> str:
        grid = [['.' for _ in range(71)] for _ in range(71)]
        for p in self.parse()[:1024]:
            grid[p.y][p.x] = '#'
        return str(self.solve(grid))

    def part2(self) -> str:
        positions = self.parse()
        grid = [['.' for _ in range(71)] for _ in range(71)]
        for i, p in enumerate(positions):
            grid[p.y][p.x] = '#'
            if i > 1024:
                if self.solve(grid) < 0:
                    return str(p)

    def parse(self) -> list[Pos]:
        ret = []
        for line in self.data_lines():
            x, y = line.split(',')
            ret.append(Pos(int(x), int(y)))
        return ret
