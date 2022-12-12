import dataclasses
import enum
from typing import Iterable, Iterator, Optional, Self


class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"
    UP_RIGHT = "UR"
    UP_LEFT = "UL"
    DOWN_RIGHT = "DR"
    DOWN_LEFT = "DL"
    STAY = ""

    def to_vector(self) -> "Position":
        x = y = 0
        if self in (Direction.UP, Direction.UP_RIGHT, Direction.UP_LEFT):
            y = 1
        if self in (Direction.DOWN, Direction.DOWN_RIGHT, Direction.DOWN_LEFT):
            y = -1
        if self in (Direction.RIGHT, Direction.UP_RIGHT, Direction.DOWN_RIGHT):
            x = 1
        if self in (Direction.LEFT, Direction.UP_LEFT, Direction.DOWN_LEFT):
            x = -1
        return Position(x, y)

    def __add__(self, other: Self) -> Self:
        vector = self.to_vector() + other.to_vector()
        return self.__class__.from_vector(vector)

    @classmethod
    def from_vector(cls, vector: "Position") -> Self:
        def _to_unit(i: int) -> int:
            if i == 0:
                return 0
            return i // abs(i)

        vector = Position(_to_unit(vector.x), _to_unit(vector.y))
        match vector:
            case Position(1, 0):
                return cls.RIGHT
            case Position(0, 1):
                return cls.UP
            case Position(-1, 0):
                return cls.LEFT
            case Position(0, -1):
                return cls.DOWN
            case Position(1, 1):
                return cls.UP_RIGHT
            case Position(1, -1):
                return cls.DOWN_RIGHT
            case Position(-1, 1):
                return cls.UP_LEFT
            case Position(-1, -1):
                return cls.DOWN_LEFT
            case Position(1, 0):
                return cls.STAY
            case _:
                raise ValueError

    @property
    def is_vertical(self) -> bool:
        return self in (Direction.UP, Direction.DOWN)


@dataclasses.dataclass
class Move:
    direction: Direction
    steps: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        direction, steps = line.split()
        return cls(direction=Direction(direction), steps=int(steps))


def moves() -> Iterator[Move]:
    with open("inputs/9_input") as f:
        for line in f:
            yield Move.from_line(line)


@dataclasses.dataclass(frozen=True)
class Position:
    x: int
    y: int

    def is_close_to(self, other: Self) -> bool:
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)

    def move(self, direction: Direction) -> Self:
        return self + direction.to_vector()

    def direction_to(self, other: Self) -> Direction:
        direction = Direction.from_vector(other - self)
        if direction.is_vertical:
            if self.x > other.x:
                direction += Direction.LEFT
            if self.x < other.x:
                direction += Direction.RIGHT
        else:
            if self.y > other.y:
                direction += Direction.DOWN
            if self.y < other.y:
                direction += Direction.UP
        return direction

    def follow(self, other: Self) -> Self:
        if self.is_close_to(other):
            return self
        return self.move(self.direction_to(other))


class Snake:
    head: Position
    tail: Optional["Snake"]

    def __init__(self, size: int):
        self.head = Position(0, 0)
        if size <= 1:
            self.tail = None
        else:
            self.tail = self.__class__(size - 1)

    def follow(self, other: Position):
        self.head = self.head.follow(other)
        if self.tail is not None:
            self.tail.follow(self.head)

    def move_one_step(self, direction: Direction):
        self.head = self.head.move(direction)
        if self.tail is not None:
            self.tail.follow(self.head)

    @property
    def tail_position(self) -> Position:
        if self.tail is None:
            return self.head
        return self.tail.tail_position

    def __str__(self) -> str:
        return f"{self.head} - {self.tail}"


class SnakeTracker:
    def __init__(self, snake: Snake):
        self.snake = snake
        self.tail_positions: set[Position] = set()

    def move_one_step(self, direction: Direction):
        self.snake.move_one_step(direction)
        self.tail_positions.add(self.snake.tail_position)

    def move(self, move: Move):
        for _ in range(move.steps):
            self.move_one_step(move.direction)
            # print(self.snake)


def part_1(moves: Iterable[Move]) -> int:
    snake = Snake(size=2)
    snake_tracker = SnakeTracker(snake)
    for move in moves:
        snake_tracker.move(move)
    return len(snake_tracker.tail_positions)


def part_2(moves: Iterable[Move]) -> int:
    snake = Snake(size=10)
    snake_tracker = SnakeTracker(snake)
    for move in moves:
        snake_tracker.move(move)
    return len(snake_tracker.tail_positions)


print("part 1:", part_1(moves()))
print("part 2:", part_2(moves()))
