from . import strongly_typed_function

import logging, time

@strongly_typed_function
def _hello(hello: str, goodbye: str):
    print(f"{hello} world!")
    time.sleep(1)
    print(f"{goodbye} world!")

@strongly_typed_function
def _must_raise(func, etype, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except etype:
        pass
    else:
        raise AssertionError("test failed!")

def test():
    hello = _hello
    hello("Starting tests,", "First one passed,")
    time.sleep(1)
    _must_raise(hello, TypeError, 2, "ji")
    _must_raise(hello, TypeError, 8, None)
    _must_raise(hello, TypeError, "hvs", goodbye=True)
    _must_raise(hello, TypeError, hello=_hello, goodbye=_hello)
    print("So did the others, world!")

test()
