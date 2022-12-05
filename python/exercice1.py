from typing import Iterable


def elves_input() -> Iterable[list[int]]:
    elf_input: list[int] = []
    with open("/home/vianney/perso/adventofcode2022/inputs/1_input") as file:
        for line in file:
            if not line.strip():
                yield elf_input
                elf_input = []
            else:
                elf_input.append(int(line.strip()))
        yield elf_input


top_three = sorted(sum(elf_input) for elf_input in elves_input())[-3:]
print(top_three)
print(sum(top_three))
