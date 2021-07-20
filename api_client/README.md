# API client

- Here we have some functions which return Studio Ghibli films.
- We define a `Film` dataclass
- Note the `undefined` parameter to `dataclass_json` which tells it to ignore any fields we haven't defined
- Then we do `Film.schema()`, this actually generates a Marshmallow schema which does JSON validation.
- So we first make an http request for the films with httpx and then let our `FilmSchema` deserialize the json into dataclass instances
- Get film works similarly except for just one film
