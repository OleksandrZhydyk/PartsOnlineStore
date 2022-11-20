import string

from django.core.exceptions import ValidationError


def part_number_validator(part_number):
    for symbol in string.ascii_uppercase:
        if symbol in part_number:
            break
    else:
        raise ValidationError("Part number has to have at least one uppercase letter")
    count = 0
    for digit in string.digits:
        if digit in part_number:
            count += part_number.count(digit)
    if count < 4:
        raise ValidationError("Part number has to have at least 4 digits")
