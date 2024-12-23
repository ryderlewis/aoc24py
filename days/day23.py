from .day import Day
from collections import defaultdict


class Day23(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        connections = self.parse()
        groups = self.find_groups(connections)
        answer = 0
        for group in groups:
            answer += self.count_chiefs(group)
        # return str(answer)
        print(f"{len(connections)=}, {len(groups)=}")
        return str(sum(len(g) for g in groups))

    def part2(self) -> str:
        return "dayXX 2"

    @staticmethod
    def count_chiefs(group: set[str]) -> int:
        """
        the number of chief groups can be calculated as the sum of N choose 3
        where N is the total number of items in the group, and we're only looking
        for subgroups with at least one chief.
        """
        num_chiefs = sum(1 for item in group if item.startswith('t'))
        num_all = len(group)

        count = 0
        while num_chiefs > 0:
            num_all -= 1
            num_chiefs -= 1
            count += num_all * (num_all-1) // 2  # num_all choose 2
        return count


    @staticmethod
    def find_groups(connections: dict[str, set[str]]) -> list[set[str]]:
        groups = []
        to_check = set(connections.keys())
        while to_check:
            item = to_check.pop()
            group = {item}
            work = [item]
            while work:
                item = work.pop()
                for next_item in connections[item]:
                    if next_item not in group:
                        group.add(next_item)
                        work.append(next_item)
                        to_check.discard(next_item)
            groups.append(group)
        return groups

    def parse(self) -> dict[str, set[str]]:
        ret: dict[str, set[str]] = defaultdict(set)
        for line in self.data_lines():
            a, b = line.split('-')
            ret[a].add(b)
            ret[b].add(a)
        return ret
