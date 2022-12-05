import dataclasses

Stack = list[str]
Stacks = list[Stack]


def init_stack(raw_stacks: list[str]) -> Stacks:
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

    def handle(self, stacks: Stacks):
        to_move = []
        for _ in range(self.move_count):
            to_move.append(stacks[self.from_stack].pop())
        stacks[self.to_stack].extend(to_move[::-1])


def readstacks(filename="./inputs/5_input") -> tuple[list[str], list[Move]]:
    with open(filename) as f:
        raw_stacks = []
        for line in f:
            if line.strip():
                raw_stacks.append(line.strip("\n"))
            else:
                break
        moves = []
        for line in f:
            moves.append(Move.from_raw(line.strip()))
        return raw_stacks, moves


raw_stacks, moves = readstacks()
stacks = init_stack(raw_stacks)

for move in moves:
    move.handle(stacks)

print("".join(stack[-1] for stack in stacks))
