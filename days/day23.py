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
        return ','.join(sorted(self.biggest_group(connections)))

    def biggest_group(self, connections: dict[str, set[str]]) -> set[str]:
        output = {}
        self.make_groups(connections, output)
        biggest = sorted(output.keys())[-1]
        for k in sorted(output.keys()):
            v = output[k]
            print(f"{k}: {len(v)}")
        return set(output[biggest].pop())

    def make_groups(
            self,
            connections: dict[str, set[str]],
            output: dict[int, set[tuple[str, ...]]],
            size: int = 1,
    ) -> None:
        for combo in combinations(sorted(connections.keys()), size):
            union = connections[combo[0]] | {combo[0]}
            for c in combo[1:]:
                union &= (connections[c] | {c})

            if len(union) >= size:
                if size >= 13:
                    un = tuple(sorted(union))
                    print(f"{combo=}, {un=}")
                changed = False
                if size not in output:
                    output[size] = set()
                for c2 in combinations(union, size):
                    t = tuple(sorted(c2))
                    if t not in output[size]:
                        changed = True
                        output[size].add(t)
                        if size >= 12:
                            print(f"{size=}, {len(output[size])=}")
                if changed:
                    self.make_groups({k: connections[k] & union for k in union}, output, size+1)


    def parse(self) -> dict[str, set[str]]:
        ret: dict[str, set[str]] = defaultdict(set)
        for line in self.data_lines():
            a, b = line.split('-')
            ret[a].add(b)
            ret[b].add(a)
        return ret
