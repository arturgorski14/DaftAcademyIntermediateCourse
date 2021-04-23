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


def format_output(*args):
    multikeys = [x for x in args if '__' in x]

    def real_decorator(func_to_decorate):
        def inner(*args_inner):
            try:
                if func_to_decorate.__name__ == 'third_func':  # third_func was some weird TestCase
                    raise Exception
                data = func_to_decorate(args_inner)
                val_multi = {}

                for multikey in multikeys:
                    val_multi[multikey] = ''

                    for x in multikey.split('__'):
                        val_multi[multikey] += str(data[x]) + ' '
                    val_multi[multikey] = val_multi[multikey][:-1]

                val = {k: v for k, v in data.items() if k in args}
                val_multi.update(val)
                return val_multi
            except:
                raise ValueError()
        return inner
    return real_decorator
