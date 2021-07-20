from dataclasses import dataclass, replace
from typing import Optional

@dataclass
class Address:
    line_1: str
    line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str

    def format(self) -> str:
        line_2 = f'{self.line_1}\n'
        line_3 = self.line_2 + "\n" if self.line_2 else ""
        line_4 = f'{self.city}, {self.state} {self.postal_code}\n'
        line_5 = self.country
        return line_2 + line_3 + line_4 + line_5


@dataclass
class Person:
    first_name: str
    last_name: str
    address: Optional[Address]

    def get_postage_label(self) -> str:
        line_1 = f'{self.first_name} {self.last_name}\n'
        return line_1 + self.address.format() if self.address else ""


if __name__ == '__main__':
    me = Person(
        "Jeremiah", "Malina",
        Address(
            "386 Park Ave S", "6th Floor",
            "New York", "New York", "33143",
            "United States of America"
        )
    )
    print(me.get_postage_label())
    print()
    old_me = replace(
        me, address=replace(
            me.address,
            line_1="235 9th St",
            line_2="Apt 1",
            city="Brooklyn",
            postal_code="11215"
        )
    )
    print(old_me.get_postage_label())

    homeless_me = Person(
        "Jeremiah", "Malina", None
    )
