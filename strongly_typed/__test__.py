from . import _hello, _must_raise

import logging, time

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
