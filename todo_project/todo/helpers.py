"""
Decorator that converts the output of a function to title case.

Args:
    fn: A callable that takes a string and returns a string.

Returns:
    A wrapper function that applies title case formatting to the result of fn.
"""

"""
Wrapper function that executes the decorated function and applies title case.

Args:
    arg: The input string to pass to the decorated function.

Returns:
    The result of the decorated function formatted in title case.
"""
"""
Decorator that strips whitespace and converts the output of a function to uppercase.

Args:
    fn: A callable that takes a string and returns a string.

Returns:
    A wrapper function that applies stripping and uppercase formatting to the result of fn.
"""

"""
Wrapper function that executes the decorated function, strips whitespace, and applies uppercase.

Args:
    arg: The input string to pass to the decorated function.

Returns:
    The result of the decorated function with whitespace stripped and converted to uppercase.
"""


from typing import Callable
def decor(fn: Callable[[str], str]) -> Callable[[str], str]:
    def wrapper(arg: str) -> str:
        func = fn(arg)
        output = func.title()
        return output
    return wrapper

@decor
def make_title(name: str) -> str:
    """
    Converts a name string to title case.

    Args:
        name: The input name string.

    Returns:
        The name formatted in title case.
    """
    
    return name

def decor_input(fn: Callable[[str], str]) -> Callable[[str], str]:
    def wrapper(arg:str)-> str:
        func = fn(arg)
        output = func.strip().upper()
        return output
    return wrapper

@decor_input
def make_upper(string: str) -> str:
    """
    Converts a string to uppercase after stripping whitespace.

    Args:
        string: The input string.

    Returns:
        The string with whitespace removed and converted to uppercase.
    """
    
    return string

if __name__ == "__main__":
    print(decor.__annotations__)
    print(make_title.__annotations__)
    print(make_title("hello there world"))
    print(decor_input.__annotations__)
    print(make_upper.__annotations__)
    print(make_upper("   hello there world   "))

