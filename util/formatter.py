import re


def remove_non_digits(string):
    return re.sub('\\D', '', string)
