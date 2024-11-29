class Day:
    def __init__(self, *, filename, part):
        self._filename = filename
        self._part = int(part)

    def run(self) -> str:
        if self._part == 1:
            return self.part1()
        else:
            return self.part2()

    def part1(self) -> str:
        return "Override me part 1"

    def part2(self) -> str:
        return "Override me part 2"

    def data(self) -> str:
        with open(self._filename, 'r') as f:
            return f.read()

    def data_lines(self) -> list[str]:
        return self.data().strip().splitlines()
