from enum import Enum
from typing import Iterable


class Play(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __gt__(self, other: "Play") -> bool:
        if self is Play.PAPER and other is Play.ROCK:
            return True
        if self is Play.ROCK and other is Play.SCISSORS:
            return True
        if self is Play.SCISSORS and other is Play.PAPER:
            return True
        return False

    @classmethod
    def from_letter(cls, letter: str) -> "Play":
        if letter in ("A", "X"):
            return cls.ROCK
        if letter in ("B", "Y"):
            return cls.PAPER
        return cls.SCISSORS

    @property
    def score(self) -> int:
        return self.value

    def score_against(self, other: "Play") -> int:
        win_score = 6 if self > other else 0
        draw_score = 3 if self is other else 0
        return self.score + win_score + draw_score


def rounds(filename="./inputs/2_input") -> Iterable[tuple[Play, Play]]:
    with open(filename) as f:
        for line in f:
            elf, me = line.strip().split()
            yield Play.from_letter(elf), Play.from_letter(me)


print(sum(me.score_against(elf) for elf, me in rounds()))
