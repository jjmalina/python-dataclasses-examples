from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
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


@dataclass_json
@dataclass
class Person:
    created_timestamp: datetime = field(
        metadata={'dataclasses_json': {
            'encoder': datetime.isoformat,
            'decoder': datetime.fromisoformat,
        }}
    )
    first_name: str
    last_name: str
    address: Optional[Address]

    def get_postage_label(self) -> str:
        line_1 = f'{self.first_name} {self.last_name}\n'
        return line_1 + self.address.format() if self.address else ""


if __name__ == '__main__':
    me = Person(
        datetime.utcnow(),
        "Jeremiah", "Malina",
        Address(
            "386 Park Ave S", "6th Floor",
            "New York", "New York", "33143",
            "United States of America"
        )
    )
    from pprint import pprint

    # https://github.com/lidatong/dataclasses-json/issues/31
    pprint(me.to_dict())  # type: ignore
    print()

    print("JSON:")
    print(me.to_json(indent=2)) # type: ignore
    print()

    data = {
        'created_timestamp': datetime.utcnow().isoformat(),
        'first_name': 'Jeremiah',
        'last_name': 'Malina',
        'address': {
            'city': 'New York',
            'state': 'New York',
            'country': 'United States of America',
            'line_1': '386 Park Ave S',
            'line_2': '6th Floor',
            'postal_code': '33143'
        }
    }
    print(Person.from_dict(data)) # type: ignore
