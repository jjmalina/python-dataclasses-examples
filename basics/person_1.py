from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str


if __name__ == '__main__':
    me: Person = Person(
        "Jeremiah", "Malina",
        "386 Park Ave S", "6th Floor",
        "New York", "New York", "10016",
        "United States of America"
    )
    print(me)

    me2 = Person(
        "Jeremiah", "Malina",
        "386 Park Ave S", "6th Floor",
        "New York", "New York", "10016",
        "United States of America"
    )
    print(me == me2)
