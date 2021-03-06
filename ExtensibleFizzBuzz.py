# A FizzBuzz program.
# Add additional criteria to this dict.

conditions_dict = {3: "Fizz", 5: "Buzz"}
start_value = 1
end_value = 100


def fizz_or_buzz(this_number: int) -> None:
    # If it meets the criteria return the word(s) else return the digit as string
    result_string = ''
    for this_value in sorted(conditions_dict):
        if not this_number % this_value:
            result_string = result_string + conditions_dict[this_value]
    if not result_string:
        result_string = str(this_number)
    print(result_string)


def main() -> None:
    for this_number in range(start_value, end_value + 1):
        fizz_or_buzz(this_number)


main()
