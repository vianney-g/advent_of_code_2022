import dataclasses
from typing import Iterable

Rucksack = str


@dataclasses.dataclass(frozen=True)
class Compartments:
    comp_1: str
    comp_2: str

    @classmethod
    def from_rucksack(cls, rucksack: Rucksack) -> "Compartments":
        middle = len(rucksack) // 2
        comp_1, comp_2 = rucksack[:middle], rucksack[middle:]
        return cls(comp_1, comp_2)

    @property
    def only_shared(self) -> str:
        commoms = set(self.comp_1).intersection(set(self.comp_2))
        return next(iter(commoms))


def priority(char: str) -> int:
    up_adj = 26 if char.isupper() else 0
    return ord(char.lower()) - ord("a") + 1 + up_adj


def rucksacks() -> Iterable[Rucksack]:
    with open("./inputs/3_input") as f:
        for line in f:
            yield line.strip()


def commons(rucksacks: Iterable[Rucksack]) -> Iterable[str]:
    for sack in rucksacks:
        yield Compartments.from_rucksack(sack).only_shared


print(sum(priority(common) for common in commons(rucksacks())))
