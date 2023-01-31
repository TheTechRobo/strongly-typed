# strongly_typed

This is a python decorator that allows you to type-check functions. Itll check the type signature of the function and, if the signature and the parameters given mismatch, will raise an exception.

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

- Return types are not tested. This may be fixed, and it might not be considered a breaking change.

- Using nested parameterized types (e.g. `Union[dict[str, list[int]]]`) will always raise an exception on 1.0, and might raise an exception on 2.0. This will hopefully be fixed before 2.0 is released.

- Using "interchangeable" types (e.g. using an int when a float is required, or vice versa) will raise an exception. **This is by design.** The whole idea is to prevent python's weak typing from screwing things up. Type coercion isn't the only way it can do that, but it's one of them - and not always caught by linters.

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
