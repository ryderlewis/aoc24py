from .day import Day
from dataclasses import dataclass

@dataclass(frozen=True)
class Lock:
    heights: tuple[int, ...]


@dataclass(frozen=True)
class Key:
    heights: tuple[int, ...]

    def fits(self, lock: Lock) -> bool:
        for x, y in zip(self.heights, lock.heights):
            if x + y > 5:
                return False
        return True


class Day25(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        locks, keys = self.parse()
        count = 0
        for lock in locks:
            for key in keys:
                if key.fits(lock):
                    count += 1
        return str(count)

    def part2(self) -> str:
        return "dayXX 2"

    def parse(self) -> tuple[list[Lock], list[Key]]:
        locks, keys = [], []
        data = self.data_lines()
        i = 0
        while i < len(data):
            line = data[i]
            i += 1
            if not line:
                continue

            is_lock = line.startswith('#')
            heights = [0] * 5
            for _ in range(5):
                line = data[i]
                i += 1
                for j, c in enumerate(line):
                    if c == '#':
                        heights[j] += 1
            i += 1
            if is_lock:
                locks.append(Lock(heights=tuple(heights)))
            else:
                keys.append(Key(heights=tuple(heights)))

        return locks, keys