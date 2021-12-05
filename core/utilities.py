import typing


def is_small_equal(num1: float, num2: float) -> bool:
    return abs(num1 - num2) <= 4


def find_close_numbers(numbers: typing.List[int]) -> typing.List[typing.List[int]]:
    close_numbers = []
    for i in range(len(numbers) - 1):
        current_number, next_number = numbers[i], numbers[i + 1]
        if is_small_equal(current_number, next_number):
            close_numbers.append([current_number, next_number])

    return close_numbers