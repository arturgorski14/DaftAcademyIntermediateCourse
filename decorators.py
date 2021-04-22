from functools import wraps  # could be useful to have
import re


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
