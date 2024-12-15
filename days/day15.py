from .day import Day
from collections import namedtuple
from enum import Enum


Pos = namedtuple('Pos', 'row col')

class Block(Enum):
    WALL = "#"
    BOX = "O"
    BOT = "@"
    BLANK = "."
    LBOX = "["
    RBOX = "]"

class Dir(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'

class Grid:
    def __init__(self, double: bool = False):
        self.blocks: dict[Pos, Block] = {}
        self.rows = 0
        self.cols = 0
        self.robot = Pos(0, 0)
        self.double = double

    def add_block(self, pos: Pos, block: Block) -> None:
        self.rows = max(pos.row+1, self.rows)
        if self.double:
            pos = Pos(pos.row, pos.col*2)
            self.cols = max(pos.col+2, self.cols)
        else:
            self.cols = max(pos.col+1, self.cols)
        if block == Block.BLANK:
            return
        self.blocks[pos] = block
        if self.double:
            if block == Block.BOX:
                self.blocks[pos] = Block.LBOX
                self.blocks[Pos(pos.row, pos.col+1)] = Block.RBOX
            elif block == Block.WALL:
                self.blocks[pos] = Block.WALL
                self.blocks[Pos(pos.row, pos.col+1)] = Block.WALL
        if block == Block.BOT:
            self.robot = pos

    def move(self, direction: Dir) -> None:
        if self.double:
            self._move_double(direction)
        else:
            self._move_single(direction)

    def _move_single(self, direction: Dir) -> None:
        r, c = self.robot.row, self.robot.col

        if direction == Dir.UP:
            while self.blocks.get(Pos(r-1, c), Block.BLANK) == Block.BOX:
                r -= 1
            if self.blocks.get(Pos(r-1, c), Block.BLANK) == Block.BLANK:
                # can move
                if r != self.robot.row:
                    self.blocks[Pos(r-1, c)] = Block.BOX
                del self.blocks[self.robot]
                self.robot = Pos(self.robot.row-1, c)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.DOWN:
            while self.blocks.get(Pos(r+1, c), Block.BLANK) == Block.BOX:
                r += 1
            if self.blocks.get(Pos(r+1, c), Block.BLANK) == Block.BLANK:
                # can move
                if r != self.robot.row:
                    self.blocks[Pos(r+1, c)] = Block.BOX
                del self.blocks[self.robot]
                self.robot = Pos(self.robot.row+1, c)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.LEFT:
            while self.blocks.get(Pos(r, c-1), Block.BLANK) == Block.BOX:
                c -= 1
            if self.blocks.get(Pos(r, c-1), Block.BLANK) == Block.BLANK:
                # can move
                if c != self.robot.col:
                    self.blocks[Pos(r, c-1)] = Block.BOX
                del self.blocks[self.robot]
                self.robot = Pos(r, self.robot.col-1)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.RIGHT:
            while self.blocks.get(Pos(r, c+1), Block.BLANK) == Block.BOX:
                c += 1
            if self.blocks.get(Pos(r, c+1), Block.BLANK) == Block.BLANK:
                # can move
                if c != self.robot.col:
                    self.blocks[Pos(r, c+1)] = Block.BOX
                del self.blocks[self.robot]
                self.robot = Pos(r, self.robot.col+1)
                self.blocks[self.robot] = Block.BOT

        else:
            raise ValueError(str(direction))

    def _can_move(self, pos: Pos, direction: Dir) -> bool:
        if direction not in (Dir.UP, Dir.DOWN):
            raise ValueError(f"Not implemented for {direction}")
        dr = 1 if direction == Dir.DOWN else -1
        npos = Pos(pos.row+dr, pos.col)

        blk = self.blocks.get(npos, Block.BLANK)
        if blk == Block.BLANK:
            return True
        elif blk == Block.WALL:
            return False
        elif blk == Block.LBOX:
            return self._can_move(npos, direction) and self._can_move(Pos(npos.row, npos.col+1), direction)
        elif blk == Block.RBOX:
            return self._can_move(npos, direction) and self._can_move(Pos(npos.row, npos.col-1), direction)
        else:
            raise RuntimeError(str(blk))

    def _do_move(self, pos: Pos, direction: Dir) -> None:
        if direction not in (Dir.UP, Dir.DOWN):
            raise ValueError(f"Not implemented for {direction}")
        dr = 1 if direction == Dir.DOWN else -1
        npos = Pos(pos.row+dr, pos.col)

        blk = self.blocks.get(npos, Block.BLANK)
        if blk == Block.BLANK:
            pass
        elif blk == Block.LBOX:
            self._do_move(npos, direction)
            self._do_move(Pos(npos.row, npos.col+1), direction)
        elif blk == Block.RBOX:
            self._do_move(npos, direction)
            self._do_move(Pos(npos.row, npos.col-1), direction)
        else:
            raise RuntimeError(str(blk))

        self.blocks[npos] = self.blocks[pos]
        del self.blocks[pos]

    def _move_double(self, direction: Dir) -> None:
        r, c = self.robot.row, self.robot.col

        if direction == Dir.UP:
            """
            ##############
            ##......##..##
            ##...[].[]..##
            ##...[][]...##
            ##....[]....##
            ##.....@....##
            ##############
            """
            if self._can_move(Pos(r, c), direction):
                self._do_move(Pos(r, c), direction)
                self.robot = Pos(self.robot.row-1, self.robot.col)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.DOWN:
            if self._can_move(Pos(r, c), direction):
                self._do_move(Pos(r, c), direction)
                self.robot = Pos(self.robot.row+1, self.robot.col)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.LEFT:
            while self.blocks.get(Pos(r, c-1), Block.BLANK) in (Block.LBOX, Block.RBOX):
                c -= 1
            if self.blocks.get(Pos(r, c-1), Block.BLANK) == Block.BLANK:
                # can move
                while c != self.robot.col:
                    self.blocks[Pos(r, c-1)] = self.blocks[Pos(r, c)]
                    c += 1
                del self.blocks[self.robot]
                self.robot = Pos(r, self.robot.col-1)
                self.blocks[self.robot] = Block.BOT

        elif direction == Dir.RIGHT:
            while self.blocks.get(Pos(r, c+1), Block.BLANK) in (Block.RBOX, Block.LBOX):
                c += 1
            if self.blocks.get(Pos(r, c+1), Block.BLANK) == Block.BLANK:
                # can move
                while c != self.robot.col:
                    self.blocks[Pos(r, c+1)] = self.blocks[Pos(r, c)]
                    c -= 1
                del self.blocks[self.robot]
                self.robot = Pos(r, self.robot.col+1)
                self.blocks[self.robot] = Block.BOT

        else:
            raise ValueError(str(direction))

    def gps_sum(self) -> int:
        return sum(100*p.row + p.col for p, b in self.blocks.items()
                   if b in (Block.BOX, Block.LBOX))

    def print(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                block = self.blocks.get(Pos(row, col), Block.BLANK)
                print(block.value, end='')
            print()


class Day15(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        grid, directions = self.parse()
        # print(f"0:")
        # grid.print()

        for s, d in enumerate(directions, 1):
            grid.move(d)
            # print(f"{s} {d}:")
            # grid.print()
        return str(grid.gps_sum())

    def part2(self) -> str:
        grid, directions = self.parse(double=True)
        # print(f"0:")
        # grid.print()

        for s, d in enumerate(directions, 1):
            grid.move(d)
            # print(f"{s} {d}:")
            # grid.print()
        return str(grid.gps_sum())

    def parse(self, double: bool = False) -> tuple[Grid, list[Dir]]:
        grid = Grid(double)
        dirs = []
        doing_grid = True

        for row, line in enumerate(self.data_lines()):
            if doing_grid and line == "":
                doing_grid = False
            elif doing_grid:
                for col, c in enumerate(line):
                    grid.add_block(Pos(row, col), Block(c))
            else:
                dirs.extend([Dir(c) for c in line])

        return grid, dirs
