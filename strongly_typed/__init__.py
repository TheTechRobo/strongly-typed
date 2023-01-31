"""
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
"""

import inspect
import logging
import time
import types
import typing

class _BuiltInTypeError(Exception):
    pass

class StronglyTypedFunction:
    def __init__(self, old, r, accept_subclasses):
        self.old = old
        self.r = r
        self.a = accept_subclasses
    def _clean_generic(self, potential_generic):
        if type(potential_generic) == types.GenericAlias:
            return typing.get_origin(potential_generic) # TODO: Recurse through the parameters. Raise _BuiltInTypeError to fail the test
        return potential_generic
    def _is_compatible(self, value, types: typing.Union[type, tuple[type]]):
        if self.a:
            if type(types) == type:
                return isinstance(value, types)
            # isinstance takes subclasses into accounts
            new_list = map(lambda i : self._clean_generic(i), types)
            return isinstance(value, tuple(new_list))
        # if there's only one type
        if type(types) == type:
            return types == type(value)
        # otherwise, there's multiple. for this we have to iterate over the types manually
        for type_ in types:
            if type(value) == type_:
                return True
        return False
    def _is_compatible_wrap(self, *args, **kwargs):
        try:
            return self._is_compatible(*args, **kwargs)
        except _BuiltInTypeError:
            return False
    def _check_type(self, value, signature):
        if typing.get_origin(signature) is typing.Union:
            return self._is_compatible_wrap(value, typing.get_args(signature))
        if signature == typing.Any:
            return True
        return self._is_compatible_wrap(value, signature)
    def __call__(self, *args, **kwargs):
        sig = inspect.signature(self.old)
        positional_counter = 0
        for name, param in sig.parameters.items():
            if param.kind == param.VAR_POSITIONAL or param.kind == param.VAR_KEYWORD:
                # not even gonna try...
                continue
            try:
                value = kwargs[name]
            except KeyError: # if it's positional
                value = args[positional_counter]
                # positional args will always be in order
                # so we just have to increment a counter
                # we can't just increment it every iteration, though, since then keyword args will increment it
                positional_counter += 1
            # re param.empty: it's supposed to be used statically but this WorksTM
            if param.annotation != param.empty and not self._check_type(value, param.annotation):
                msg = f"Invalid type for param {name} - expected {type(value)}, got {param.annotation}"
                if self.r:
                    raise TypeError(msg)
                logging.warning(msg)
        # FIXME: check return value too
        self.old(*args, **kwargs)


class _decorator:
    def __init__(self, raise_exception, allow_subclasses):
        self.raise_exception = raise_exception
        self.allow_subclasses = allow_subclasses
    def __call__(self, func):
        return StronglyTypedFunction(func, self.raise_exception, self.allow_subclasses)

def strongly_typed(*, raise_exception=True, allow_subclasses=True):
    """
    Intended for use as a decorator.
    func (Callable): The function to modify. This is automatically done for you when using as a decorator.
    raise_exception (bool): If true, will raise TypeError on type mismatch. Otherwise, will use logging.warning on type mismatch.
    allow_subclasses (bool): If true, subclasses will be permitted. This was not the case in 1.0, but that violated Python's spec.
    """
    return _decorator(raise_exception=raise_exception, allow_subclasses=allow_subclasses)
