from enum import Enum
from operator import gt, is_, lt
from typing import Iterable


class Strategy(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    @property
    def operator(self):
        ops = {Strategy.LOSE: lt, Strategy.DRAW: is_, Strategy.WIN: gt}
        return ops[self]


class Play(Enum):
    ROCK = "A"
    PAPER = "B"
    SCISSORS = "C"

    def __gt__(self, other: "Play") -> bool:
        if self is Play.PAPER and other is Play.ROCK:
            return True
        if self is Play.ROCK and other is Play.SCISSORS:
            return True
        if self is Play.SCISSORS and other is Play.PAPER:
            return True
        return False

    @property
    def score(self) -> int:
        scores = {Play.ROCK: 1, Play.PAPER: 2, Play.SCISSORS: 3}
        return scores[self]

    def score_against(self, other: "Play") -> int:
        win_score = 6 if self > other else 0
        draw_score = 3 if self is other else 0
        return self.score + win_score + draw_score

    def from_strategy(self, strategy: Strategy) -> "Play":
        for play in Play:
            if strategy.operator(play, self):
                return play
        raise ValueError(f"Invalid strategy {strategy}")


def rounds(filename="./inputs/2_input") -> Iterable[tuple[Play, Play]]:
    with open(filename) as f:
        for line in f:
            elf, strategy = line.strip().split()
            elf_play = Play(elf)
            yield elf_play, elf_play.from_strategy(Strategy(strategy))


print(sum(me.score_against(elf) for elf, me in rounds()))
