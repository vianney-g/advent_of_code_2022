from typing import Iterable

Rucksack = str
PackOf3 = tuple[Rucksack, Rucksack, Rucksack]


def priority(char: str) -> int:
    up_adj = 26 if char.isupper() else 0
    return ord(char.lower()) - ord("a") + 1 + up_adj


def rucksacks() -> Iterable[Rucksack]:
    with open("./inputs/3_input") as f:
        for line in f:
            yield line.strip()


def rucksacks_by_3(
    rucksacks: Iterable[Rucksack],
) -> Iterable[PackOf3]:
    sacks = iter(rucksacks)
    while True:
        try:
            yield (next(sacks), next(sacks), next(sacks))
        except StopIteration:
            break


def badges(packs: Iterable[PackOf3]) -> Iterable[str]:
    for sack1, sack2, sack3 in packs:
        candidates = set(sack1) & set(sack2) & set(sack3)
        yield next(iter(candidates))


print(sum(priority(badge) for badge in badges(rucksacks_by_3(rucksacks()))))
