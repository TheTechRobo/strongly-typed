# strongly_typed

This is a python decorator that allows you to type-check functions. Itll check the type signature of the function and, if the signature and the parameters given mismatch, will raise an exception.

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

## Known issues
`*args` and `**kwargs` are not tested at all. This is because I'm not sure how I'd implement that. (Plus, I don't think it's very common to annotate those.)

## Contributing
The code is probably terrible. Please help me fix it! If you have any suggestions, please let me know.

## Licence

> Copyright 2023 TheTechRobo
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>    http://www.apache.org/licenses/LICENSE-2.0
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

