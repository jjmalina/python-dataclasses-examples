from dataclasses import dataclass
from typing import final, Generic, TypeVar, Callable

T = TypeVar('T')


class List(Generic[T]):
    @classmethod
    def create(cls, *args):
        if not args:
            return Nil()
        else:
            return Cons(args[0], cls.create(*args[1:]))


@final
class Nil(List[T]):
    pass


@dataclass(frozen=True)
class Cons(List[T]):
    head: T
    tail: List[T]


B = TypeVar('B')


def fold_right(ll: List[T], z: B, op: Callable[[T,B],B]) -> B:
    match ll:
        case Nil():
            return z
        case Cons(h, t):
            return op(h, fold_right(t, z, op))


def main():
    mylist: List[int] = List.create(1, 2, 5.0)
    print(fold_right(mylist, 0, lambda v, acc: acc + v))
    other: List[int] = List.create("h", "e", "l", "l", "o", "!")
    print(fold_right(other, "", lambda v, acc:  v + acc))


if __name__ == '__main__':
    main()
