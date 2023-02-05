# strongly_typed

This is a python decorator that allows you to type-check functions. Itll check the type signature of the function and, if the signature and the parameters or return value given mismatch, will raise an exception at runtime.

## Python versions
The module currently supports only Python 3.9+ to keep the code nice and simple, and being able to use the latest typing features. Changing this is a breaking change and will have a Semver major version bump.

1.0 officially supported 3.8+, but might have supported earlier versions.

2.0 (and the master branch) will officially support 3.9+.

## Inspiration
I wanted to use this to make sure that software i was going to write was resilient for data integrity reasons. I've also learned a lot about decorators, etc.

## Usage

```python
from strongly_typed import strongly_typed
@strongly_typed
def add(a: int, b: int, message_template: str):
    result = a + b
    message = message_template % result
    return message

add(1, 2, "The answer is %s!")
add(1, "e", 5) # raises an exception!
```

See `help(strongly_typed)` for details on decorator. Note that default behaviour changed in 2.0 - now, so as to not violate Python's spec, subclasses are permitted. To get back old behaviour, use `@strongly_typed(allow_subclasses=False)`.

## Known issues
- `*args` and `**kwargs` are not tested at all. This is because I'm not sure how I'd implement that. (Plus, I don't think it's very common to annotate those.)

- Using nested parameterized types (e.g. `Union[dict[str, list[int]]]`) will always raise an exception on 1.0, and might raise an exception on 2.0. This will hopefully be fixed before 2.0 is released.

- `NewType`s are checked, but only the parent. So:

```python
Type = NewType("Type", int)

@strongly_typed
def test(e: Type):
    pass
    
test(Type(5)) # OK
test(5) # OK - according to Python's spec, should not be
test(Type("this is a string")) # Raises exception, as it should
test("this is another string") # Raises exception, as it should
```

This may be fixed without it being considered a breaking change.

- Using "interchangeable" types (e.g. using an int when a float is required, or vice versa) will raise an exception. **This is by design.** The whole idea is to prevent python's weak typing from screwing things up. Type coercion isn't the only way it can do that, but it's one of them - and not always caught by linters. `None` is also not allowed. To get around this, try using a `typing.Union` (or, for `None`, a `typing.Optional`).

## Release notes
GitHub releases will be created for future releases, but I'll provide some changelog here for people reading on PyPI.

### 1.0
Initial release

### 1.0.1
Set up PyPI, clarify stuff in README

*some post releases were made to address issues and typos with documentation*

### 2.0 (unreleased currently)
- Add support for the typing module.
- Fix keyword arguments.
- Require decorator options to be passed as keyword arguments.
- Use more sane defaults. (please reread docs)
- Remove `strongly_typed_function` alias for the decorator.
- Check return values.
- Add support for class methods and instance methods.

## Contributing
The code is probably terrible. Please help me fix it! If you have any suggestions, please let me know. Pull requests are obviously welcome.

## Licence

```
Copyright 2023 TheTechRobo
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
