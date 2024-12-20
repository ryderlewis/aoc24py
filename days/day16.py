from .day import Day
from collections import namedtuple
import heapq

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
    ) -> int:
        pos = self._find_start(maze)
        work = [(0, pos, EAST)]
        seen = {(pos, EAST): 0}
        while work:
            score, pos, direction = heapq.heappop(work)
            if maze[pos.row][pos.col] == 'E':
                return score

            # try going straight
            npos = Pos(pos.row + DIRS[direction][0], pos.col + DIRS[direction][1])
            if (npos, direction) not in seen or seen[(npos, direction)] > score+1:
                if maze[npos.row][npos.col] != '#':
                    seen[(npos, direction)] = score+1
                    heapq.heappush(work, (score + 1, npos, direction))

            # and turn left/right
            for delta in (-1, 1):
                d = (direction + delta) % len(DIRS)
                if (pos, d) not in seen or seen[(pos, d)] > score+1000:
                    seen[(pos, d)] = score + 1000
                    heapq.heappush(work, (score + 1000, pos, d))

    def part1(self) -> str:
        return str(self.shortest(self.parse()))

    def all_the_shortest(
            self,
            maze: tuple[tuple[str, ...], ...],
            target: int,
            steps: set[Pos],
            score: int,
            pos: Pos,
            direction: int,
            answer: set[Pos]
    ) -> None:
        my_steps = {pos}
        my_steps.update(steps)
        if score > target:
            return
        elif score == target:
            if maze[pos.row][pos.col] == 'E':
                answer.update(my_steps)
                print(f"found one - {len(answer)=}")
            return

        # try going straight
        npos = Pos(pos.row + DIRS[direction][0], pos.col + DIRS[direction][1])
        if npos not in my_steps:
            if maze[npos.row][npos.col] != '#':
                self.all_the_shortest(maze, target, my_steps, score+1, npos, direction, answer)

        # and turn left/right
        for delta in (-1, 1):
            d = (direction + delta) % len(DIRS)
            npos = Pos(pos.row + DIRS[d][0], pos.col + DIRS[d][1])
            if npos not in my_steps:
                if maze[npos.row][npos.col] != '#':
                    self.all_the_shortest(maze, target, my_steps, score+1001, npos, d, answer)

    def part2(self) -> str:
        target = self.shortest()
        maze = self.parse()
        pos = self._find_start(maze)
        answer: set[Pos] = set()
        self.all_the_shortest(maze, target, set(), 0, pos, EAST, answer)
        return str(len(answer))

    def parse(self) -> tuple[tuple[str, ...], ...]:
        return tuple([tuple(line) for line in self.data_lines()])