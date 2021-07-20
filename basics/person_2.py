from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class Person:
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str

    def get_postage_label(self) -> str:
        line_1 = f'{self.first_name} {self.last_name}\n'
        line_2 = f'{self.address_line_1}\n'
        line_3 = self.address_line_2 + "\n"
        line_4 = f'{self.city}, {self.state} {self.postal_code}\n'
        line_5 = self.country
        return line_1 + line_2 + line_3 + line_4 + line_5


if __name__ == '__main__':
    me = Person(
        "Jeremiah", "Malina",
        "386 Park Ave S", "6th Floor",
        "New York", "New York", "10016",
        "United States of America"
    )
    print(me.get_postage_label())
    print()

    # old_me which is bad
    # old_me = me
    # old_me.address_line_1 = "235 9th St"
    # old_me.address_line_2 = "Apt 1"
    # old_me.city = "Brooklyn"
    # old_me.postal_code = "11215"

    old_me = replace(
        me, address_line_1="235 9th St",
        address_line_2="Apt 1",
        city="Brooklyn", postal_code="11215")
    print(old_me.get_postage_label())
