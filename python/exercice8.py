from typing import Iterator

TreeMap = list[list[int]]
Position = tuple[int, int]


def build_map() -> list[list[int]]:
    tree_map = []
    with open("./inputs/8_input") as f:
        for line in f:
            trees_line = [int(i) for i in line.strip()]
            tree_map.append(trees_line)
    return tree_map


def get_visibles(trees_map: TreeMap) -> Iterator[Position]:
    for y, line in enumerate(trees_map):
        for x, height in enumerate(line):
            if all(h < height for h in line[:x]):
                yield (y, x)
            elif all(h < height for h in line[x + 1 :]):
                yield (y, x)
            elif all(h < height for h in (trees_map[col][x] for col in range(0, y))):
                yield (y, x)
            elif all(
                h < height
                for h in (trees_map[col][x] for col in range(y + 1, len(trees_map)))
            ):
                yield (y, x)


def count_visible(height, others: list[int]) -> int:
    count = 0
    for other in others:
        count += 1
        if other >= height:
            break
    return count


def number_of_visibles(trees_map: TreeMap) -> int:
    return sum(1 for _ in get_visibles(trees_map))


def scenic_scores(trees_map: TreeMap) -> Iterator[int]:
    for y, line in enumerate(trees_map):
        for x, height in enumerate(line):
            yield (
                count_visible(height, line[x - 1 :: -1] if x else [])
                * count_visible(height, line[x + 1 :])
                * count_visible(height, [trees_map[n][x] for n in range(y)][::-1])
                * count_visible(
                    height, [trees_map[n][x] for n in range(y + 1, len(trees_map))]
                )
            )


if __name__ == "__main__":
    trees_map = build_map()
    print("Part1, number_of_visibles =", number_of_visibles(trees_map))
    print("Part2, best scenic score =", max(scenic_scores(trees_map)))
