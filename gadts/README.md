# GADTs or Generalized algebraic datatypes

Python's dataclasses can be leveraged to use GADTs. We have an example here of a `Maybe` type and a singly linked `List` type.

With pattern matching (which will be GA in Python 3.10) we can implement functions/methods on these GADTs which provide a more composable interface to using them. Unfortunately mypy doesn't support pattern matching yet so it doesnt't work on this code.

The `Maybe` type can have a function applied to it with with `map` if it has a value, otherwise nothing happens. This makes handling values which have a type of `Option[A]` where `A` can be any type much easier. You no longer have to write `some_optional_field if some_optional_field else ""` it's just `some_optional_field.get_or_else("")` and if you want to modify the value you can use `map` before the `get_or_else`.

The `List` type is a less practical example in Python because we already have `list`, it just shows how you can define a generic data type that can be operated on with pattern matching.

The [returns](https://returns.readthedocs.io/en/latest/index.html) library implements a `Maybe` type like we have here. There's also a [Result](https://returns.readthedocs.io/en/latest/pages/result.html) type which can be either a `Success` with a value or a `Failure` with an exception and this allows you to write referentially transparent code.
