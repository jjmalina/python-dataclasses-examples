# Modeling people with dataclasses

## Person v1

- Annotate a class with @dataclass
- Write the fields and their types
- Initialize the dataclass with data (order matters). I'm using the office address to not doxx myself
- We run mypy to check the code and then run the code.

## Person v2

- Now we've added a method to get the text for a postage label.
- There's actually a bug in `get_postage_label`, can you spot it?
- Another thing, te code under old_me doesn't work! That's because we have `frozen=True`
- So dataclasses can be made immutable
- If you want to change the value of a field, you can use `replace`

## Person v3

- Ok so now we decided to factor out address into another dataclass
- A person may not necessarily have an address so we can easily handle that
- The homeless version of me, needs an explicit None.
- We could make it a default None in the dataclass
- Fields with defaults have to go after fields without defaults (like kwargs after args)
- We could use `dataclasses.field` to provide a callable function to provide a default for a field (good for non primitive defaults)

## Person v4

- Here we're taking a person and converting them to a dict using `asdict`
- Notice that this will dictify the nested address dataclass
- We can use this to serialize dataclasses to json
- However, going from json/dict to a dataclass instance is not so simple

## Person v5

- This is where we have to bring in [dataclasses-json](https://github.com/lidatong/dataclasses-json)
- We can also add a `created_timestamp` field which is a datetime and still deserialize from json or serialize to json
- dataclasses-json will also handle the nested `Address` type for us!
