from .day import Day


class Day05(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        pairs, books = self.parse()
        ret = 0
        for book in books:
            if self.is_correct(pairs, book):
                ret += book[len(book)//2]
        return str(ret)

    def part2(self) -> str:
        pairs, books = self.parse()
        ret = 0
        for book in books:
            if self.is_correct(pairs, book):
                continue
            # make the book correct
            pages = list(book)
            need_change = True
            while need_change:
                need_change = False
                for i in range(len(pages)-1):
                    for j in range(i+1, len(pages)):
                        if pages[i] in pairs.get(pages[j], set()):
                            # j needs to be moved before i
                            need_change = True
                            val = pages.pop(j)
                            pages[i:i] = [val]
                            break
                    if need_change:
                        break
            ret += pages[len(pages)//2]
        return str(ret)

    @staticmethod
    def is_correct(pairs: dict[int, set[int]], book: tuple[int, ...]):
        for i in range(len(book)-1):
            for j in range(i+1, len(book)):
                if book[j] in pairs and book[i] in pairs[book[j]]:
                    return False
        return True

    def parse(self) -> tuple[dict[int, set[int]], list[tuple[int, ...]]]:
        pairs, books = {}, []
        for line in self.data_lines():
            if '|' in line:
                a, b = map(int, line.split('|'))
                pairs.setdefault(a, set())
                pairs[a].add(b)
            elif ',' in line:
                books.append(tuple(map(int, line.split(','))))
        return pairs, books
