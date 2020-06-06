from typing import List


def fib(i):
    if i == 0:
        return 1
    if i == 1:
        return 1
    else:
        return fib(i - 1) + fib(i - 2)


# noinspection PyUnusedLocal
def main(*args: List[str]):
    return fib(5)
