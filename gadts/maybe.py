from dataclasses import dataclass, replace
from typing import Callable, final, Generic, TypeVar


A = TypeVar('A')
B = TypeVar('B')

@dataclass
class Maybe(Generic[A]):
    def map(self, f: Callable[[A], B]) -> 'Maybe[B]':
        match self:
            case Nothing():
                return Nothing()
            case Just(value):
                return Just(f(value))

    def get_or_else(self, v: A) -> A:
        match self:
            case Nothing():
                return v
            case Just(value):
                return value


@final
class Nothing(Maybe[A]):
    pass


@dataclass
class Just(Maybe[A]):
    value: A


@dataclass
class Person:
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: Maybe[str]
    city: str
    state: str
    postal_code: str
    country: str

    def get_postage_label(self) -> str:
        line_1 = f'{self.first_name} {self.last_name}\n'
        line_2 = f'{self.address_line_1}\n'
        line_3 = self.address_line_2.map(
            lambda a2: f"{a2}\n").get_or_else("")
        line_4 = f'{self.city}, {self.state} {self.postal_code}\n'
        line_5 = self.country
        return line_1 + line_2 + line_3 + line_4 + line_5


if __name__ == '__main__':
    v: Maybe[int] = Just(5)
    print(v.map(lambda a: a + 1))

    x: Maybe[int] = Nothing()
    print(x.map(lambda a: a + 1))
    print()

    me = Person(
        "Jeremiah", "Malina",
        "386 Park Ave S", Nothing(),
        "New York", "New York", "10016",
        "United States of America"
    )
    print(me.get_postage_label())
    print()
    old_me = replace(
        me, address_line_1="235 9th St",
        address_line_2=Just("Apt 1"),
        city="Brooklyn", postal_code="11215")
    print(old_me.get_postage_label())
