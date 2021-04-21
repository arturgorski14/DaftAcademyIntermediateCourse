from functools import wraps  # could be useful to have


def greetings(function_to_greet):
    def inner(names: str):
        return f'Hello {function_to_greet(names).title()}'
    return inner
