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

    def part1(self) -> str:
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
        zwires = sorted([w for w in self.wires if w.startswith('z')], reverse=True)
        zvals = ''.join(str(self.wires[z].output) for z in zwires)
        return str(int(zvals, 2))

    def part2(self) -> str:
        return "dayXX 2"

    def parse_wires(self) -> dict[str, Wire]:
        ret = {}
        for line in self.data_lines():
            if ': ' in line:
                name, val = line.split(': ')
                ret[name] = Wire(name=name, output=int(val))
        return ret

    def parse_gates(self, wires: dict[str, Wire]) -> list[Gate]:
        ret = []
        for line in self.data_lines():
            if ' -> ' in line:
                gates, out_wire = line.split(' -> ')
                w1, op, w2 = gates.split()
                wire1 = wires.setdefault(w1, Wire(name=w1))
                wire2 = wires.setdefault(w2, Wire(name=w2))
                out_wire = wires.setdefault(out_wire, Wire(name=out_wire))
                ret.append(Gate(in1=wire1, in2=wire2, out=out_wire, op=Op(op.lower())))
        return ret
