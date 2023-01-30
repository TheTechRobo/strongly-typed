import inspect, logging, time

def strongly_typed(func, raise_exception=True):
    """
    Intended for use as a decorator.
    func (Callable): The function to modify. This is automatically done for you when using as a decorator.
    raise_exception (bool): If true, will raise TypeError on type mismatch. Otherwise, will use logging.warning on type mismatch.
    """
    class StronglyTypedFunction:
        def __init__(self, old, r):
            self.old = old
            self.r = r
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
                # re param.empty: it's not intended to be used that way but It Works TM
                if type(value) != param.annotation and param.annotation != param.empty:
                    msg = f"Invalid type for param {name} - expected {type(value)}, got {param.annotation}"
                    if self.r:
                        raise TypeError(msg)
                    logging.warning(msg)
            self.old(*args, **kwargs)
    return StronglyTypedFunction(func, raise_exception)

strongly_typed_function = strongly_typed


