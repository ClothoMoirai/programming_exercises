#!/usr/bin/python3
# Return the product of two numbers unless that result is greater than 1000.
# If greater than 1000, return the sum. From: https://pynative.com/python-basic-exercise-for-beginners/
from typing import List
threshold = 1000


def get_input() -> str:
    return input('Please enter a number: ')


def check_number(my_number: str) -> bool:
    return my_number.isnumeric()


def str_to_int(my_number: str) -> int:
    return int(my_number)


def get_numbers() -> List[int]:
    number_list = []
    while len(number_list) < 2:
        this_number = get_input()
        if check_number(this_number):
            number_list.append(str_to_int(this_number))
    return number_list


def compute_result(my_numbers: List[int]) -> int:
    result = my_numbers[0] * my_numbers[1]
    if result > threshold:
        result = my_numbers[0] + my_numbers[1]
    return result


def main():
    my_list = get_numbers()
    my_number = compute_result(my_list)
    print(my_number)


main()
