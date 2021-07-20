"""
An API client for Studio Ghibli films: https://ghibliapi.herokuapp.com/#tag/Films
"""
import httpx
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from typing import List


# https://github.com/lidatong/dataclasses-json#handle-unknown--extraneous-fields-in-json
@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Film:
    id: str
    title: str
    original_title: str
    description: str
    director: str
    producer: str
    release_date: str
    running_time: str
    rt_score: str
    people: List[str]
    species: List[str]
    locations: List[str]
    vehicles: List[str]
    url: str


FilmSchema = Film.schema() # type: ignore

API_URL = 'https://ghibliapi.herokuapp.com/films'


def get_films() -> List[Film]:
    resp = httpx.get(API_URL)
    return FilmSchema.loads(resp.text, many=True)


def get_film(id: str) -> Film:
    resp = httpx.get(f'{API_URL}/{id}')
    return FilmSchema.loads(resp.text)


if __name__ == '__main__':
    films = get_films()
    from pprint import pprint
    pprint(films)
    print("Single film:")
    import random
    random_film_id = random.choice(films).id
    film = get_film(random_film_id)
    pprint(film)
