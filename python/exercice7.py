import dataclasses
from functools import cached_property, singledispatch
from typing import Iterator, Optional


class Ls:
    ...


@dataclasses.dataclass
class File:
    name: str
    size: int


DirName = str


class UnknownDir(Exception):
    ...


@dataclasses.dataclass
class Dir:
    name: DirName
    parent: Optional["Dir"] = None
    subdirs: list["Dir"] = dataclasses.field(default_factory=list)
    files: list[File] = dataclasses.field(default_factory=list)

    @cached_property
    def size(self) -> int:
        return sum(f.size for f in self.files) + sum(d.size for d in self.subdirs)

    def up(self) -> "Dir":
        return self.parent if self.parent else self

    def into(self, dirname: DirName) -> "Dir":
        try:
            return next(d for d in self.subdirs if d.name == dirname)
        except StopIteration:
            raise UnknownDir(dirname)

    def add_subdir(self, dirname: DirName) -> "Dir":
        try:
            return self.into(dirname)
        except UnknownDir:
            subdir = self.__class__(dirname, parent=self)
            self.subdirs.append(subdir)
            return subdir

    def __iter__(self) -> Iterator["Dir"]:
        yield self
        for subdir in self.subdirs:
            yield from subdir

    def __gt__(self, other: "Dir") -> bool:
        return self.size < other.size

    @property
    def path(self) -> str:
        if self.parent:
            return f"{self.parent.path}/{self.name}"
        return ""

    def __str__(self) -> str:
        return f"{self.path} - {self.size}"


@dataclasses.dataclass
class Cd:
    dirname: DirName

    def execute(self, current_dir: Dir) -> Dir:
        if self.dirname == "..":
            return current_dir.up()
        if self.dirname == ".":
            return current_dir
        return current_dir.into(self.dirname)


def listing() -> Iterator[Cd | Ls | File | DirName]:
    with open("./inputs/7_input") as f:
        cd_prefix, ls_prefix = "$ cd ", "$ ls"
        for line in f:
            line = line.strip()
            if line.startswith(cd_prefix):
                yield Cd(line.removeprefix(cd_prefix))
            elif line.startswith(ls_prefix):
                yield Ls()
            else:
                filetype_or_size, filename = line.split(maxsplit=1)
                if filetype_or_size == "dir":
                    yield DirName(filename)
                else:
                    yield File(filename, int(filetype_or_size))


ROOT_DIR = Dir("/")


@singledispatch
def handle(invalid, current_dir: Dir) -> Dir:
    raise ValueError(f"Unknown entry {invalid}")


@handle.register
def _(cd: Cd, current_dir: Dir) -> Dir:
    match cd:
        case Cd(DirName("/")):
            return ROOT_DIR
        case _:
            return cd.execute(current_dir)


@handle.register
def _(_: Ls, current_dir: Dir) -> Dir:
    return current_dir


@handle.register
def _(file_: File, current_dir: Dir) -> Dir:
    current_dir.files.append(file_)
    return current_dir


@handle.register
def _(dirname: DirName, current_dir: Dir) -> Dir:
    current_dir.add_subdir(dirname)
    return current_dir


def build_filesystem():
    current_dir = ROOT_DIR

    for entry in listing():
        current_dir = handle(entry, current_dir)


def small_sizes(max_size: int = 100_000) -> Iterator[Dir]:
    return (dir_ for dir_ in ROOT_DIR if dir_.size <= max_size)


def eligible_dir_freeing(missing_space: int) -> Iterator[Dir]:
    return (dir_ for dir_ in ROOT_DIR if dir_.size >= missing_space)


if __name__ == "__main__":
    build_filesystem()
    print("Part 1, total sum of small dirs:", sum(dir_.size for dir_ in small_sizes()))

    needed_space = 30_000_000
    total_space = 70_000_000
    used_space = ROOT_DIR.size
    available_space = total_space - used_space
    missing_space = needed_space - available_space
    eligible = sorted(eligible_dir_freeing(missing_space), reverse=True)
    print("Part 2, Candidate for suppression:", eligible[0])
