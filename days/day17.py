from .day import Day
from enum import Enum

class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

class Machine:
    def __init__(self, a: int, b: int, c: int, program: tuple[int, ...]):
        self._a = a
        self._b = b
        self._c = c
        self.program = program

    def _combo(self, v: int) -> int:
        if 0 <= v <= 3:
            return v
        elif v == 4:
            return self.a
        elif v == 5:
            return self.b
        elif v == 6:
            return self.c
        else:
            raise ValueError(v)

    def run(self, part2: int = 0, a_override: int | None = None) -> str:
        ret = []
        pc = 0
        prog = self.program
        self.a = self._a
        self.b = self._b
        self.c = self._c
        if a_override is not None:
            self.a = a_override

        while 0 <= pc < len(prog):
            op = Opcode(prog[pc])
            lit = prog[pc+1]
            com = self._combo(lit) if lit != 7 else 0
            pc += 2

            if op == Opcode.ADV:
                self.a = self.a // (2**com)
            elif op == Opcode.BXL:
                self.b = self.b ^ lit
            elif op == Opcode.BST:
                self.b = com % 8
            elif op == Opcode.JNZ:
                if self.a != 0:
                    pc = lit
            elif op == Opcode.BXC:
                self.b = self.b ^ self.c
            elif op == Opcode.OUT:
                ret.append(com % 8)
            elif op == Opcode.BDV:
                self.b = self.a // (2**com)
            elif op == Opcode.CDV:
                self.c = self.a // (2**com)

        if part2:
            if tuple(ret) == prog[-part2:]:
                return "ok"
            return ""
        else:
            return ','.join(map(str, ret))


class Day17(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        machine = self.parse()
        return machine.run()

    def nested(self, machine: Machine, answer: int = 0, depth: int = 1) -> int | None:
        answer *= 8
        for a in range(8):
            if machine.run(part2=depth, a_override=answer+a) == "ok":
                if depth == len(machine.program):
                    return answer+a
                elif (recur := self.nested(machine, answer+a, depth+1)) is not None:
                    return recur
        return None

    def part2(self) -> str:
        machine = self.parse()
        return str(self.nested(machine))

    def parse(self) -> Machine:
        a, b, c = 0, 0, 0
        prog = (0,)
        for line in self.data_lines():
            if not line:
                continue
            label, value = line.split(': ')
            if label == 'Register A':
                a = int(value)
            if label == 'Register B':
                b = int(value)
            if label == 'Register C':
                c = int(value)
            if label == 'Program':
                prog = tuple(map(int, value.split(',')))
        return Machine(a, b, c, prog)
