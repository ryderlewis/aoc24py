from .day import Day


class Day02(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        safe_count = 0
        for line in self.data_lines():
            n = list(map(int, line.split()))
            if (all(1 <= n[i] - n[i-1] <= 3 for i in range(1, len(n))) or
                    all(1 <= n[i-1] - n[i] <= 3 for i in range(1, len(n)))):
                safe_count += 1
        return str(safe_count)

    def part2(self) -> str:
        safe_count = 0
        for line in self.data_lines():
            nums = list(map(int, line.split()))
            for x in range(len(nums)):
                n = nums[:x] + nums[x+1:]
                if (all(1 <= n[i] - n[i-1] <= 3 for i in range(1, len(n))) or
                        all(1 <= n[i-1] - n[i] <= 3 for i in range(1, len(n)))):
                    safe_count += 1
                    break
        return str(safe_count)
