import dataclasses
import enum
import operator
from itertools import groupby
from typing import Callable, Iterable, Iterator, Literal, Self


class Operator(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"

    @property
    def callable(self) -> Callable[[int, int], int]:
        match self:
            case Operator.PLUS:
                return operator.add
            case Operator.MINUS:
                return operator.sub
            case Operator.MUL:
                return operator.mul


@dataclasses.dataclass
class Operation:
    operator: Operator
    left: int | Literal["old"]
    right: int | Literal["old"]

    def execute(self, old: int) -> int:
        to_call = self.operator.callable
        left = old if self.left == "old" else self.left
        right = old if self.right == "old" else self.right
        return to_call(left, right)

    @classmethod
    def from_str(cls, op_str: str) -> Self:
        op_str = op_str.removeprefix("new = ")
        left, op, right = op_str.split()
        return cls(
            operator=Operator(op),
            left="old" if left == "old" else int(left),
            right="old" if right == "old" else int(right),
        )


@dataclasses.dataclass
class Divisible:
    by: int

    def __call__(self, integer: int) -> bool:
        return integer % self.by == 0


@dataclasses.dataclass
class Monkey:
    id_: int
    items: list[int]
    operation: Operation
    test: Divisible
    if_true_monkey_id: int
    if_false_monkey_id: int
    inspected_count: int = 0

    @classmethod
    def from_lines(cls, lines: Iterator[str]) -> Self:
        striped_lines: Iterator[str] = (line.strip() for line in lines)
        id_ = int(next(striped_lines).removeprefix("Monkey ").removesuffix(":"))
        items = [
            int(item)
            for item in next(striped_lines).removeprefix("Starting items: ").split(",")
        ]
        operation = Operation.from_str(next(striped_lines).removeprefix("Operation: "))
        test = Divisible(
            by=int(next(striped_lines).removeprefix("Test: divisible by "))
        )
        if_true = int(next(striped_lines).split()[-1])
        if_false = int(next(striped_lines).split()[-1])
        return cls(
            id_=id_,
            items=items,
            operation=operation,
            test=test,
            if_true_monkey_id=if_true,
            if_false_monkey_id=if_false,
        )

    def inspect_item(
        self,
        item: int,
        registry: Callable[[int], "Monkey"],
        extra_rule: Callable[[int], int],
    ):
        worry_level = self.operation.execute(item)
        worry_level = extra_rule(worry_level)
        throw_to = (
            self.if_true_monkey_id
            if self.test(worry_level)
            else self.if_false_monkey_id
        )
        registry(throw_to).items.append(worry_level)
        self.inspected_count += 1

    def play_round(
        self, registry: Callable[[int], "Monkey"], extra_rule: Callable[[int], int]
    ):
        while self.items:
            item, *self.items = self.items
            self.inspect_item(item, registry, extra_rule)


def parse_monkeys(filename: str) -> Iterator[Monkey]:
    with open(filename) as lines:
        is_empty = lambda line: not bool(line.split())
        for is_blank, monkey_lines in groupby(lines, key=is_empty):
            if not is_blank:
                yield Monkey.from_lines(monkey_lines)


class MonkeysRepository:
    def __init__(self):
        self._monkeys: list[Monkey] = []

    def read_file(self, filename: str):
        with open(filename) as lines:
            is_empty = lambda line: not bool(line.split())
            for is_blank, monkey_lines in groupby(lines, key=is_empty):
                if not is_blank:
                    self._monkeys.append(Monkey.from_lines(monkey_lines))

    @classmethod
    def from_file(cls, filename: str = "./inputs/11_input") -> Self:
        repo = cls()
        repo.read_file(filename)
        return repo

    @property
    def divprod(self) -> int:
        def mul(it: Iterable[int]) -> int:
            res = 1
            for i in it:
                res *= i
            return res

        return mul(m.test.by for m in self)

    def get(self, monkey_id: int) -> Monkey:
        return next(m for m in self if m.id_ == monkey_id)

    def __len__(self) -> int:
        return len(self._monkeys)

    def __iter__(self) -> Iterator[Monkey]:
        return iter(self._monkeys)


def part_1(monkeys: MonkeysRepository):
    def extra_rule(worry_level: int) -> int:
        return worry_level // 3

    for _ in range(20):
        for id_ in range(len(monkeys)):
            monkeys.get(id_).play_round(monkeys.get, extra_rule)

    sorted_inspections = sorted(m.inspected_count for m in monkeys)
    print(sorted_inspections[-1] * sorted_inspections[-2])


def part_2(monkeys: MonkeysRepository):
    divprod = monkeys.divprod

    def extra_rule(worry_level: int) -> int:
        return worry_level % divprod

    for _ in range(10_000):
        for id_ in range(len(monkeys)):
            monkeys.get(id_).play_round(monkeys.get, extra_rule)

    sorted_inspections = sorted(m.inspected_count for m in monkeys)
    print(sorted_inspections[-1] * sorted_inspections[-2])


if __name__ == "__main__":
    part_1(MonkeysRepository.from_file())
    part_2(MonkeysRepository.from_file())
