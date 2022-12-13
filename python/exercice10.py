import dataclasses
from collections.abc import Iterable, Iterator
from typing import Protocol


@dataclasses.dataclass
class Registry:
    value: int


class Command(Protocol):
    def execute(self, registry: Registry) -> Iterator:
        ...


SignalStrength = int


class Machine:
    def __init__(self):
        self.registry = Registry(1)
        self.cycle: int = 0

    def execute(self, command: Command) -> Iterator[SignalStrength]:
        for _ in command.execute(self.registry):
            self.cycle += 1
            self.draw_pixel()
            yield self.signal_strength

    @property
    def sprite_position(self) -> tuple[int, int, int]:
        pt = self.registry.value
        return (pt, pt + 1, pt + 2)

    def draw_pixel(self):
        crt = self.cycle % 40
        pixel = "#" if crt in self.sprite_position else "."
        end = "" if crt else "\n"
        print(pixel, end=end)

    @property
    def signal_strength(self) -> SignalStrength:
        if (self.cycle - 20) % 40:
            return 0
        return self.registry.value * self.cycle


machine = Machine()


@dataclasses.dataclass
class Addx:
    value: int

    def execute(self, registry: Registry) -> Iterator:
        yield
        yield
        registry.value += self.value


class Noop:
    def execute(self, registry: Registry) -> Iterator:
        yield

    def __str__(self) -> str:
        return "Noop"


def commands() -> Iterable[Command]:
    with open("./inputs/10_input") as lines:
        for line in lines:
            line = line.strip()
            if line == "noop":
                yield Noop()
            else:
                _, value = line.split()
                yield Addx(int(value))


def signal_strengths(commands: Iterable[Command]) -> Iterable[SignalStrength]:
    for cmd in commands:
        yield from machine.execute(cmd)


def part1(commands: Iterable[Command]) -> int:
    return sum(signal_strengths(commands))


print(part1(commands()))
