# People API using flask

## Schemas

- So now we're going to write an REST API server for people using flask
- First we define our dataclass, and instead of dataclasses-json we use marshmallow_dataclass because it integrates more nicely with Marshmallow which we want to do our data validation

## Database

- We're going to use Flask-SQLAlchemy with SQLite
- `Person` is our SQLAlchemy model (yeah, the name could be swapped with PersonModel)
- Then we have some functions which do CRUD operations on a Person

## API server

- First we create some error handlers to handle data validation, integrity, and not found errors
- After that we have our REST API routes
- Note the use of `@marshal_with` which uses our marshmallow schema to serialize the data we return
- In `new_person` and `update_person` we parse the JSON input and have the schema deserialize it. If any validation errors or database errors are raised they'll be caught by the error handlers to return a useful error to the API client


## Documentation

- Here we use Flask-APISpec to register our routes to generate Documentation
- If you visit http://localhost:5000/docs you'll see all our routes with their methods as well as the schemas
- The routes are missing examples and I'm not sure why

# People API using fastapi

I wanted to show the equivalent code for this people API using FastAPI because it's a hot new Python server framework that lets you write an async HTTP server.

## Schemas

- First off we're using Pydantic which is basically like Marshmallow, but instead of using a dataclass we define a Pydantic "model". It's basically a dataclass but has more features.
- The `Config` class has an `orm_mode` setting which lets Pydantic models load from ORM models like SQLAlchemy using attributes rather than accessing dictionaries

## Database

- We use `create_async_engine` and `AsyncSession` for our SQLAlchemy database setup
- I had to add `expire_on_commit=False` to `sessionmaker` in order to get the queries to work
- In the CRUD functions, note that the SQLAlchemy session is not global, it has to be passed in
- Instead of using the models to generate the queries, we have to use the SQLAlchemy core API (`select`, `update`, `delete`) to generate the queries and then execute them, and await the statement execution as well as the session commit
- SQLite with SQLAlchemy requires you to fetch to check if a record exists before running an update, and then you also have to fetch to return the changed record


## API server

- We're defining the same routes as in the Flask example except the details are slightly different
- To use the database FastAPI uses `Depends` to inject the database session into the body of the route function
- Instead of using the `@marshal_with` decorator, FastAPI has marshalling built into the route definitions by using `response_model` and it tightly integrates with Pydantic
- In `new_person` and `update_person` the `person` argument has a Pydantic model as its type, and FastAPI uses this to deserialize the input from the HTTP request
- So FastAPI has a clean input and output interface built into it whereas Flask requires you to bring a library like Marshmallow and/or Webargs
- We don't have to write error handling for validation, but we do for the 404 message
- When you run the server, it uses uvicorn which is like uWSGI but for async Python


# Conclusion

As you can see from both examples, the dataclass (whether its an actual dataclass or a library with the same syntax) is responsible for modeling our domain and representing the input and output of the server. Since our data model has type annotations, we can leverage mypy to check our code. If there was more code between the input layer and the database, we'd benefit more from type checking. The edge of our type checking is where we convert data into SQLAlchemy code, or SQLAlchemy code into data, so we have to pay attention at these boundaries to ensure that typechecking still works. So if you have a more complicated database layer, it may be worth it to load the data into dataclasses. If we pay attention to how data is transferred between the I/O boundaries of our program and make sure that the tranformations are type-checked, then everything in between those boundaries written by us should be correct assuming it passes type checks and the libraries used there have types which are correct.

## Flask vs FastAPI

Comparing the two frameworks wasn't the main goal of this excercise but here are some thoughts:

- Flask is more modular and you can swap out different extensions or libraries, but they don't necessarily work as well together
- FastAPI on the other hand has input validation and output serialization built-in with Pydantic
- FastAPI allows you to use `async` but it's a fundamentally different server so must be scaled differently compared to uWSGI
- `async def` functions return an asynchronous generator but with mypy you use the type inside of that as the return type. if your code was async but didn't use await then you'd have to wrap your return type with `typing.AsyncGenerator`
- FastAPI was built with typing in mind so mypy works better with it. Though overall mypy is still not necessarily adopted in libraries that you may use so you may be missing type safety in your project without realizing it.
- FastAPI generates API documentation for you and it works very well
- Flask is well documented, but FastAPI seems to be even more well documented with clear guides
- FastAPI appears to be faster than Flask in the benchmarks that are presented by them
- FastAPI is mostly written by one guy who has a lot of sponsorship, whereas Flask belongs to a bigger organization (used to also just be one guy ;))
- async support in sqlalchemy and other database libraries is fairly new so it may not be GA quality yet (asyncio + SQLAlchemy is in beta)

If I were to start a new API server project today I think I would go with FastAPI because of the better mypy integration and the clearer documentation. The performance is also a bonus. However I'd be a little cautious before going all-in on FastAPI because I don't have as much experience scaling an async Python server as I do using NGINX + uWSGI with Flask.

## Further Reading

- https://threeofwands.com/why-i-use-attrs-instead-of-pydantic/
