from .day import Day
from collections import defaultdict
from itertools import combinations


class Day23(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        connections = self.parse()
        count = 0
        for combo in combinations(connections.keys(), 3):
            a, b, c = sorted(combo)
            if any(x.startswith('t') for x in combo):
                if b in connections[a] and c in connections[a] and c in connections[b]:
                    count += 1
        return str(count)

    def part2(self) -> str:
        connections = self.parse()
        largest = sorted(connections.keys(), key=lambda x: -len(connections[x]))
        for k in largest:
            print(f"{k}: {len(connections[k])}")
        return "dayXX 2"

    @staticmethod
    def biggest_group(connections: dict[str, set[str]], group: set[str]) -> set[str]:
        pass

    def parse(self) -> dict[str, set[str]]:
        ret: dict[str, set[str]] = defaultdict(set)
        for line in self.data_lines():
            a, b = line.split('-')
            ret[a].add(b)
            ret[b].add(a)
        return ret
