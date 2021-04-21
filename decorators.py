from functools import wraps  # could be useful to have


def greetings(function_to_greet):
    def inner(*args):
        val = f'Hello {function_to_greet("".join(args)).title()}'
        return val
    return inner
