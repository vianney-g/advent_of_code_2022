import dataclasses
from typing import Iterable

Stack = list[str]


def init_stack(raw_stacks: list[str]) -> list[Stack]:
    iterable = iter(raw_stacks[::-1])
    number_of_stacks = len(next(iterable).split())
    stacks = [[] for _ in range(number_of_stacks)]
    for line in iterable:
        for i, item in enumerate(iter(line[1::4])):
            if item.strip():
                stacks[i].append(item)
    return stacks


@dataclasses.dataclass
class Move:
    move_count: int
    from_stack: int
    to_stack: int

    @classmethod
    def from_raw(cls, sentence: str) -> "Move":
        count, from_stack, to_stack = sentence.split()[1::2]
        return cls(
            move_count=int(count),
            from_stack=int(from_stack) - 1,
            to_stack=int(to_stack) - 1,
        )

    def handle(self, stacks: list[Stack]):
        for _ in range(self.move_count):
            stacks[self.to_stack].append(stacks[self.from_stack].pop())


def moves(raw_moves) -> Iterable[Move]:
    for raw_move in raw_moves:
        yield Move.from_raw(raw_move)


def readstacks(filename="./inputs/5_input") -> tuple[list[str], list[str]]:
    with open(filename) as f:
        raw_stacks = []
        for line in f:
            if line.strip():
                raw_stacks.append(line.strip("\n"))
            else:
                break
        moves = []
        for line in f:
            moves.append(line.strip())
        return raw_stacks, moves


raw_stacks, raw_moves = readstacks()
stacks = init_stack(raw_stacks)

for move in moves(raw_moves):
    move.handle(stacks)

print("".join(stack[-1] for stack in stacks))
