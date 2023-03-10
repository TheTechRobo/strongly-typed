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

import sys
import collections
import inspect
import logging
import time
import types
import typing
import functools

class _YouShouldNeverSeeThisError(Exception):
    """
    Raise this in a type-checking method to make the test immediately fail.
    It's called this because this exception should never escape internal code.
    """
    pass

class TypeMismatchError(TypeError):
    """
    Raised by strongly-typed when a type signature mismatch occurs.
    """
    pass

class StronglyTypedFunction(typing.Callable):
    """
    A function that is strongly typed.
    This isn't so much a function as it is a callable - i.e., a class with a __call__ method.
    """
    def __init__(self, old, r, accept_subclasses):
        self.old = old
        self.r = r
        self.a = accept_subclasses
    def _clean_generic(self, potential_generic):
        if type(potential_generic) is types.GenericAlias:
            logging.warning("GenericAlias was found. Only a shallow check will be performed.")
            return typing.get_origin(potential_generic) # TODO: Recurse through the parameters. Raise _YouShouldNeverSeeThisError to fail the test
        return potential_generic
    def _is_compatible(self, value, types_to_check: typing.Union[type, tuple[type]]):
        if self.a:
            if type(types_to_check) is type:
                return isinstance(value, types_to_check)
            if type(types_to_check) is types.GenericAlias:
                types_to_check = [types_to_check]
            # isinstance takes subclasses into accounts
            new_list = map(self._clean_generic, types_to_check)
            return isinstance(value, tuple(new_list))
        # if there's only one type
        if type(types_to_check) == type:
            return types_to_check == type(value)
        # otherwise, there's multiple. for this we have to iterate over the types manually
        for type_ in types_to_check:
            if type(value) == type_:
                return True
        return False
    def _is_compatible_wrap(self, *args, **kwargs):
        try:
            return self._is_compatible(*args, **kwargs)
        except _YouShouldNeverSeeThisError:
            return False
    def _get_callable_signature_list(self):
        if sys.version_info[1] == 9: # python 3.9 compatibility
            return types.FunctionType, StronglyTypedFunction # NewType is not a class in Python 3.9
        return types.FunctionType, StronglyTypedFunction, typing.NewType
    def _check_type(self, value, signature):
        if typing.get_origin(signature) is typing.Union:
            return self._is_compatible_wrap(value, typing.get_args(signature))
        if typing.get_origin(signature) is collections.abc.Callable:
            return hasattr(value, "__call__")
        if isinstance(signature, typing.TypeVar):
            logging.warning("TypeVar type was passed. These are not checked by strongly-typed at the moment.")
            return True
        if isinstance(signature, self._get_callable_signature_list()):
            if hasattr(signature, "__supertype__"):
                # (Regarding the signature = signature.__supertype__ line...)
                # FIXME: NO, THAT'S WRONG! I'm not even sure if there's a decent way to check this at runtime.
                # The problem is that a NewType("example", int) should be allowed as an int (which this does),
                # but not vice versa (an int should not be allowed as a NewType("example", int)!
                # However, this will catch SOME issues, and shouldnt have any false positives, so it's fine "for now".
                logging.warning("NewType was passed. The checks for NewType are not perfect and may not see any problem in some cases!.")
                return self._check_type(value, signature.__supertype__) # This is also not perfect: typing.Any etc should not be used in NewType
            else:
                raise TypeError("a function was passed as a type argument - this will cause a crash")
        if signature == typing.Any:
            return True
        return self._is_compatible_wrap(value, signature)
    def __call__(self, *args, **kwargs):
        sig = inspect.signature(self.old)
        positional_counter = 0
        for name, param in sig.parameters.items():
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                # not even gonna try...
                continue
            try:
                value = kwargs[name]
            except KeyError: # if it's positional
                try:
                    value = args[positional_counter]
                except IndexError:
                    raise TypeMismatchError(f"argument {name} appears to be missing")
                # positional args will always be in order
                # so we just have to increment a counter
                # we can't just increment it every iteration, though, since then keyword args will increment it
                positional_counter += 1
            # re param.empty: it's supposed to be used statically but this WorksTM
            if param.annotation != param.empty and not self._check_type(value, param.annotation):
                namee = getattr(param.annotation, "__name__", str(type(param.annotation)))
                msg = f"Invalid type for param {name} - expected {namee}, got {type(value)}"
                if self.r:
                    raise TypeMismatchError(msg)
                logging.warning(msg)
        ret = self.old(*args, **kwargs)
        if sig.return_annotation != inspect.Signature.empty and not self._check_type(ret, sig.return_annotation):
            name = getattr(sig.return_annotation, "__name__", str(type(sig.return_annotation)))
            msg = f"Invalid type for return value - expected {name}, got {type(ret)}"
            if self.r:
                raise TypeMismatchError(msg)
            logging.warning(msg)

def strongly_typed(func=None, *, raise_exception=True, allow_subclasses=True):
    """
    Intended for use as a decorator.
    func (Callable): The function to modify. This is automatically done for you when using as a decorator.
    raise_exception (bool): If true, will raise TypeMismatchError on type mismatch. Otherwise, will use logging.warning on type mismatch.
    allow_subclasses (bool): If true, subclasses will be permitted. This was not the case in 1.0, but that violated Python's spec.
    """
    if func:
        c = StronglyTypedFunction(func, raise_exception, allow_subclasses)
        def run(*args, **kwargs):
            return c(*args, **kwargs)
        run.__name__ = getattr(func, "__name__", run.__name__)
        run.is_strongly_typed = True
        return run
    return functools.partial(strongly_typed, raise_exception=raise_exception, allow_subclasses=allow_subclasses)
