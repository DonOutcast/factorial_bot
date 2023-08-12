def validate_number_of_factorial(string_number: str) -> bool:
    try:
        int(string_number)
        result = True
    except ValueError:
        result = False
    return result
