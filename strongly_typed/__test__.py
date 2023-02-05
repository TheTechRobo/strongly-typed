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

from . import strongly_typed as strongly_typed_function
from . import TypeMismatchError

import logging, time, typing

@strongly_typed_function
def _hello(hello: str, goodbye: str):
    print(f"{hello} world!")
    time.sleep(1)
    print(f"{goodbye} world!")


nt1 = typing.NewType("nt1", int)
@strongly_typed_function
def goodbye(hello: nt1):
    pass

#@strongly_typed_function
def _must_raise(func, etype, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except etype:
        pass
    else:
        raise AssertionError("test failed, did not raise!")

@strongly_typed_function
def _union_test(a: typing.Union[int, str], b: typing.Optional[list[None]]):
    pass

@strongly_typed_function
def _any_test(a: typing.Any):
    pass

@strongly_typed_function
def callable_test(a: typing.Callable):
    pass

@strongly_typed_function
def return_fail() -> str:
    return 2

@strongly_typed_function
def return_success() -> typing.Union[str, int]:
    return 2

@strongly_typed_function
def return_success2() -> int:
    return 4

T = typing.TypeVar("T")

@strongly_typed_function
def typevar(x: T):
    pass

@strongly_typed_function
def list_text(x: list[str]):
    pass

class LetsTestAClass:
    @strongly_typed_function
    def run(self, e: int):
        pass

    @classmethod
    @strongly_typed_function
    def run1(cls, e: int):
        pass

    @staticmethod
    @strongly_typed_function
    def run2(e: int):
        pass

class Subclass(LetsTestAClass): pass

def test_the_class():
    obj = LetsTestAClass()
    obj.run(5)
    obj.run2(5)
    _must_raise(obj.run, TypeMismatchError, "string!")

    LetsTestAClass.run1(5)
    _must_raise(LetsTestAClass.run1, TypeMismatchError, "string")
    LetsTestAClass.run2(3)

@strongly_typed_function(raise_exception=False)
def no_raise(e: int):
    pass

@strongly_typed_function(allow_subclasses=False)
def no_subclasses(x: LetsTestAClass):
    pass

@strongly_typed_function
def yes_subclasses(x: LetsTestAClass):
    pass

assert yes_subclasses.is_strongly_typed == True

def test():
    list_text(["hi", "bye"])
    goodbye(nt1(5))
    no_subclasses(LetsTestAClass())
    _must_raise(no_subclasses, TypeMismatchError, Subclass())
    yes_subclasses(LetsTestAClass())
    yes_subclasses(Subclass())
    no_raise(5)
    no_raise(None)
    hello = _hello
    hello("Starting tests,", "First one passed,")
    test_the_class()
    _any_test(True)
    _any_test(None)
    _any_test("e")
    time.sleep(1)
    _union_test("hi", [None])
    _union_test(54, [])
    typevar(None)
    callable_test(lambda : None)
    return_success()
    return_success2()
    _must_raise(list_text, TypeMismatchError, "str")
    #_must_raise(list_text, TypeMismatchError, [5, 2]) # currently does not raise even though it should
    #_must_reaise(goodbye, TypeError, 5) # currently does not raise even though it should
    _must_raise(goodbye, TypeMismatchError, "str lol")
    _must_raise(callable_test, TypeMismatchError, None)
    _must_raise(return_fail, TypeMismatchError)
    _must_raise(hello, TypeMismatchError, 2, "ji") # gotta also test the subclass that's actually raised!
    _must_raise(hello, TypeMismatchError, 8, None)
    _must_raise(hello, TypeMismatchError, "hvs", goodbye=True)
    _must_raise(hello, TypeMismatchError, hello=_hello, goodbye=_hello)
    _must_raise(_union_test, TypeMismatchError, None, [])
    print("So did the others, world!")

test()
