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

    @staticmethod
    def _find_end(grid: tuple[tuple[str, ...], ...]) -> Pos:
        for row, squares in enumerate(grid):
            for col, square in enumerate(squares):
                if square == 'E':
                    return Pos(row, col)
        raise RuntimeError("Did not find end")

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
            # random.shuffle(deltas)

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

    def all_dists(
            self,
            maze: tuple[tuple[str, ...], ...],
            starting_pos: Pos,
            *,
            reverse: bool = False,
            pointing: int = EAST,
    ) -> dict[tuple[Pos, int], int]:
        pos = starting_pos
        work = [(0, pos, pointing)]
        seen = {}
        while work:
            score, pos, direction = heapq.heappop(work)
            if (s := seen.get((pos, direction), None)) is not None:
                if s <= score:
                    continue
            seen[(pos, direction)] = score

            deltas = [-1, 0, 1]
            for delta in deltas:
                if delta == 0:
                    # try going straight
                    if reverse:
                        npos = Pos(pos.row - DIRS[direction][0], pos.col - DIRS[direction][1])
                    else:
                        npos = Pos(pos.row + DIRS[direction][0], pos.col + DIRS[direction][1])

                    if maze[npos.row][npos.col] != '#':
                        heapq.heappush(work, (score + 1, npos, direction))
                else:
                    # and turn left/right
                    d = (direction + delta) % len(DIRS)
                    heapq.heappush(work, (score + 1000, pos, d))
        return seen

    def part1(self) -> str:
        return str(self.shortest(self.parse())[0])

    def part2(self) -> str:
        maze = self.parse()
        start_pos = self._find_start(maze)
        end_pos = self._find_end(maze)

        start_dists = self.all_dists(maze, start_pos)
        ed_east = self.all_dists(maze, end_pos, reverse=True, pointing=EAST)
        ed_west = self.all_dists(maze, end_pos, reverse=True, pointing=WEST)
        ed_north = self.all_dists(maze, end_pos, reverse=True, pointing=NORTH)
        ed_south = self.all_dists(maze, end_pos, reverse=True, pointing=SOUTH)
        end_dists = {k: min(ed_east[k], ed_west[k], ed_north[k], ed_south[k]) for k in ed_east}

        best_dist = end_dists[(start_pos, EAST)]
        all_points = {start_pos}
        for (pos, direction), dist_to_end in end_dists.items():
            dist_from_start = start_dists[(pos, direction)]
            total_dist = dist_from_start + dist_to_end
            assert total_dist >= best_dist
            if total_dist == best_dist:
                all_points.add(pos)
        return str(len(all_points))

    def parse(self) -> tuple[tuple[str, ...], ...]:
        return tuple([tuple(line) for line in self.data_lines()])