from .day import Day
from dataclasses import dataclass
from enum import Enum


@dataclass
class Wire:
    name: str
    output: int|None = None


class Op(Enum):
    AND = "and"
    OR = "or"
    XOR = "xor"

    def symbol(self) -> str:
        if self == Op.AND:
            return '∧'
        elif self == Op.OR:
            return '∨'
        elif self == Op.XOR:
            return '⊕'
        else:
            raise ValueError(f'unknown operator {self}')


@dataclass
class Gate:
    in1: Wire
    in2: Wire
    out: Wire
    op: Op


class Day24(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wires = self.parse_wires()
        self.gates = self.parse_gates(self.wires)

    def reset(self, x: int, y: int) -> None:
        for w in self.wires:
            if w[0] not in ('x', 'y'):
                self.wires[w].output = None
        for a in range(45):
            self.wires[f"x{a:02d}"].output = x & 1
            self.wires[f"y{a:02d}"].output = y & 1
            x //= 2
            y //= 2

    def add(self, x: int|None = None, y: int|None=None) -> int:
        if x is not None and y is not None:
            self.reset(x, y)
        changes = True
        while changes:
            changes = False
            for g in self.gates:
                if g.out.output is None and g.in1.output is not None and g.in2.output is not None:
                    changes = True
                    if g.op == Op.AND:
                        g.out.output = g.in1.output & g.in2.output
                    if g.op == Op.OR:
                        g.out.output = g.in1.output | g.in2.output
                    if g.op == Op.XOR:
                        g.out.output = g.in1.output ^ g.in2.output
        return self.zval()

    def xval(self) -> int:
        xwires = sorted([w for w in self.wires if w.startswith('x')], reverse=True)
        xvals = ''.join(str(self.wires[x].output) for x in xwires)
        return int(xvals, 2)

    def yval(self) -> int:
        ywires = sorted([w for w in self.wires if w.startswith('y')], reverse=True)
        yvals = ''.join(str(self.wires[y].output) for y in ywires)
        return int(yvals, 2)

    def zval(self) -> int:
        zwires = sorted([w for w in self.wires if w.startswith('z')], reverse=True)
        zvals = ''.join(str(self.wires[z].output) for z in zwires)
        return int(zvals, 2)

    def part1(self) -> str:
        return str(self.add())

    def part2(self) -> str:
        """
        For this, we're going to try creating logic equations for each of the outputs,
        z00 through z45. Hopefully a pattern will emerge and it can be used to detect
        miswires.
        """
        equations = {
            f"z{z:02d}": self.logic_equation(f"z{z:02d}")
            for z in range(46)
        }
        remainders = {
            k: self.remainder_equation(k, v)
            for k, v in equations.items()
        }

        for i in range(1, 46):
            z_gate = f"z{i:02d}"
            z_prior_gate = f"z{i-1:02d}"
            eq = equations[z_gate].replace(remainders[z_prior_gate], f"r{i-1:02d}")
            print(f"{z_gate}={eq}")

        return ""

    def logic_equation(self, out_wire: str) -> str:
        """
        find the equation solely in terms of x and y input values
        of the z output value
        """
        if out_wire.startswith('x') or out_wire.startswith('y'):
            return out_wire
        z_wire = self.wires[out_wire]
        z_gate = next((g for g in self.gates if g.out is z_wire), None)
        assert z_gate is not None

        op1, op2 = sorted([
            self.logic_equation(z_gate.in1.name),
            self.logic_equation(z_gate.in2.name),
        ])

        return ''.join([
            '(',
            op1,
            z_gate.op.symbol(),
            op2,
            ')',
        ])

    @staticmethod
    def remainder_equation(val: str, eq: str) -> str:
        """
        find the least-nested xor symbol and replace with and symbol
        """
        nest = 0
        pos = None
        for i, c in enumerate(eq):
            if c == '(':
                nest += 1
            elif c == ')':
                nest -= 1
            elif c == Op.XOR.symbol():
                if nest == 1:
                    assert pos is None
                    pos = i

        if pos is None:
            return "ERR"

        assert pos is not None, f"{val=}, {eq=}"
        return ''.join([
            eq[:pos],
            Op.AND.symbol(),
            eq[pos+1:],
        ])

    def first_broken_bit(self) -> int:
        for x in range(46):
            a, b = 0, 1<<x
            c, d = 1<<x, 0
            e, f = 1<<x, 1<<x
            g, h = e*2-1, f*2-1
            try:
                if self.add(a, b) != a+b or self.add(c, d) != c+d or self.add(e, f) != e+f or self.add(g, h) != g+h:
                    return x
            except ValueError:
                return 0

    def parse_wires(self) -> dict[str, Wire]:
        ret = {}
        for line in self.data_lines():
            if ': ' in line:
                name, val = line.split(': ')
                ret[name] = Wire(name=name, output=int(val))
        return ret

    def parse_gates(self, wires: dict[str, Wire]) -> list[Gate]:
        ret = []
        remaps = {
            'z18': 'hmt',
            'hmt': 'z18',
            'bfq': 'z27',
            'z27': 'bfq',
            'z31': 'hkh',
            'hkh': 'z31',
            'bng': 'fjp',
            'fjp': 'bng',
        }
        print(','.join(sorted(remaps)))
        for line in self.data_lines():
            if ' -> ' in line:
                gates, out_wire = line.split(' -> ')
                if out_wire in remaps:
                    out_wire = remaps[out_wire]
                w1, op, w2 = gates.split()
                wire1 = wires.setdefault(w1, Wire(name=w1))
                wire2 = wires.setdefault(w2, Wire(name=w2))
                out_wire = wires.setdefault(out_wire, Wire(name=out_wire))
                ret.append(Gate(in1=wire1, in2=wire2, out=out_wire, op=Op(op.lower())))
        return ret
