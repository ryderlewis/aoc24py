from .day import Day
from collections import defaultdict, namedtuple


FPos = namedtuple('FPos', ('file_id', 'index', 'size'))
Gap = namedtuple('Gap', ('index', 'size'))

class Day09(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        compressed = self.parse()
        file_id = 0
        file = []
        is_file = True
        for d in compressed:
            if is_file:
                for _ in range(d):
                    file.append(file_id)
                file_id += 1
            else:
                for _ in range(d):
                    file.append(None)
            is_file = not is_file

        head = compressed[0]
        tail = len(file)-1
        while head < tail:
            if file[head] is not None:
                head += 1
                continue
            if file[tail] is None:
                file = file[:tail]
                tail -= 1
                continue
            file[head] = file[tail]
            file = file[:tail]
            head += 1
            tail -= 1

        ret = 0
        for i, d in enumerate(file):
            ret += i * d
        return str(ret)

    def part2(self) -> str:
        compressed = self.parse()
        file_id = 0
        file = []
        is_file = True
        gaps: list[Gap] = []
        fpos: list[FPos] = []
        for d in compressed:
            if is_file:
                if d > 0:
                    fpos.append(FPos(file_id, len(file), d))
                for _ in range(d):
                    file.append(file_id)
                file_id += 1
            else:
                if d > 0:
                    gaps.append(Gap(len(file), d))
                for _ in range(d):
                    file.append(None)
            is_file = not is_file

        while fpos:
            fp = fpos.pop()
            # find a gap for fp
            gap = None
            for i in range(len(gaps)):
                if gaps[i].index > fp.index:
                    break

                if gaps[i].size >= fp.size:
                    gap = gaps[i]
                    if gap.size > fp.size:
                        smaller_gap = Gap(gap.index + fp.size, gap.size - fp.size)
                        gaps[i] = smaller_gap
                    else:
                        gaps.pop(i)
                    break
            if gap:
                file[gap.index:gap.index+fp.size] = file[fp.index:fp.index+fp.size]
                file[fp.index:fp.index+fp.size] = [None for _ in range(fp.size)]

        ret = 0
        for i, d in enumerate(file):
            if d is not None:
                ret += i * d
        return str(ret)

    def parse(self) -> list[int]:
        return [int(c) for c in self.data_lines()[0]]
