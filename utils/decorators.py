from utils.decorators_impl import greetings, is_palindrome, format_output, add_class_method, add_instance_method, ExampleClass

# ----------------------------- 2_A_jak_art -----------------------------
@greetings
def get_names_surname(names_surname: str) -> str:
    return names_surname


@is_palindrome
def sentence(text: str) -> str:
    return text


@format_output("first_name__last_name", "city")
def first_func(*args):
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


@format_output("first_name", "age")
def second_func(*args):
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


@add_class_method(ExampleClass)
def cls_method():
    return "Hello from class!"


@add_instance_method(ExampleClass)
def inst_method():
    return "Hello from instance!"
