from .day import Day
from collections import defaultdict


class Day22(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def next_secret(num: int) -> int:
        num = ((num * 64) ^ num) % 16777216
        num = ((num // 32) ^ num) % 16777216
        num = ((num * 2048) ^ num) % 16777216
        return num

    def secret_gen(self, num: int) -> tuple[int, ...]:
        ret = [num]
        for _ in range(2000):
            ret.append(self.next_secret(ret[-1]))
        return tuple(ret)

    def part1(self) -> str:
        nums = self.parse()
        for _ in range(2000):
            for i in range(len(nums)):
                nums[i] = self.next_secret(nums[i])
        return str(sum(nums))

    def part2(self) -> str:
        nums = self.parse()
        seq_sums = defaultdict(int)

        for num in nums:
            my_seqs = {}
            all_nums = self.secret_gen(num)
            for i in range(4, len(all_nums)):
                seq = tuple([(all_nums[j]%10) - (all_nums[j+1]%10) for j in range(i-4, i)])
                if seq not in my_seqs:
                    my_seqs[seq] = all_nums[i] % 10
            for k, v in my_seqs.items():
                seq_sums[k] += v

        return str(max(seq_sums.values()))

    def parse(self) -> list[int]:
        return [int(line) for line in self.data_lines()]
