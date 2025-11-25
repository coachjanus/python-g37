from typing import Callable


def decor(fn: Callable[[str], str]) -> Callable[[str], str]:
    def wrapper(arg: str) -> str:
        func = fn(arg)
        output = func.title()
        return output
    return wrapper

@decor
def make_title(name: str) -> str:
    return name

def decor_input(fn: Callable[[str], str]) -> Callable[[str], str]:
    def wrapper(arg:str)-> str:
        func = fn(arg)
        output = func.strip().upper()
        return output
    return wrapper

@decor_input
def make_upper(string:str)-> str:
    return string

if __name__ == "__main__":
    # print(make_title("hello there world"))
    print(decor_input.__annotations__)
    print(make_upper.__annotations__)
    print(make_upper("   hello there world   "))

