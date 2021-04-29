from functools import wraps  # could be useful to have
from itertools import chain
import re
from typing import List


def greetings(function_to_greet):
    def inner(names: str):
        return f'Hello {function_to_greet(names).title()}'
    return inner


def is_palindrome(func_to_decorate):
    def inner(arg):
        orig = func_to_decorate(arg)
        val = (''.join(re.findall('[a-zA-Z0-9]+', orig))).lower()
        return f'{orig} - is {"" if val==val[::-1] else "not "}palindrome'
    return inner


def format_output(*required_keys):
    def decorator(func):
        def build_value(keys: List[List[str]], source_dict: dict):
            values = [source_dict[key] for key in keys]
            return " ".join(values)

        def wrapper(*args):
            dec_arguments = [required_key.split("__") for required_key in required_keys]
            func_output = func(*args)

            if not all(k in func_output.keys() for k in set(chain(*dec_arguments))):
                raise ValueError

            new_output = {}
            for (idx, dec_argument) in enumerate(dec_arguments):
                value = build_value(dec_argument, func_output)
                new_output[required_keys[idx]] = value

            return new_output
        return wrapper
    return decorator


class ExampleClass:
    pass


def add_class_method(cls):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


def add_instance_method(cls):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator
