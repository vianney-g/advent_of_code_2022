import collections
from itertools import islice

with open("./inputs/6_input") as file:
    line = file.readline()


def window(it, n):
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


for i, win in enumerate(window(iter(line), 14)):
    if len(set(win)) == 14:
        print(i + 14)
        break
