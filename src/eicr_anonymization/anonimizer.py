from datetime import datetime, timedelta
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase

from eicr_anonymization.element_parser import Element


def _get_leading_trailing_whitespace(value: str) -> tuple[str, str]:
    """Get the leading and trailing whitespace from a string."""
    leading_whitespace = value[: -len(value.lstrip())]
    trailing_whitespace = value[len(value.rstrip()) :]

    return leading_whitespace, trailing_whitespace


def _match_whitespace(old_value: str, new_value: str) -> str:
    """Match the whitespace of the old value to the new value."""
    leading_whitespace, trailing_whitespace = _get_leading_trailing_whitespace(old_value)
    return leading_whitespace + new_value + trailing_whitespace


def _match_case(value: str, new_value: str):
    """Match the case of the new value to the original value."""
    if value.isupper():
        return new_value.upper()
    elif value.islower():
        return new_value.lower()
    # elif value.istitle():
    #     return new_value.title()
    else:
        return new_value


def _match_punctuation(value: str, new_value: str):
    """Match the punctuation of the old value to the new value."""
    if "." not in value:
        return new_value.replace(".", "")
    elif value.endswith(".") and not new_value.endswith("."):
        return new_value + "."
    else:
        return new_value


def _match_formatting(old_value: str, new_value: str) -> str:
    return _match_case(
        old_value, _match_whitespace(old_value, _match_punctuation(old_value, new_value))
    )


def _normalize_value(value: str):
    """Normalize the value by removing leading and trailing whitespace and converting to lowercase."""
    return value.lower().strip().replace(".", "")

def _compare_normalized_values(old_value: str, new_value: str):
    """Compare the normalized values of the old and new values."""
    return _normalize_value(old_value) == _normalize_value(new_value)

def _is_in_replacements(value: str, replacements: dict[str, str]):
    """Check if a replacement is needed."""
    return any(
        _compare_normalized_values(value, replacement)
        for replacement in replacements.values()
    )




class Anonymizer:
    """Anonymizes the data."""

    def __init__(self):
        """Initialize the Anonymizer class."""
        SECONDS_IN_100_YEARS = int(100 * 60 * 60 * 24 * 365.25)
        # The main offset is a random number of seconds between 0 and 100 years
        self.time_offset = randint(0, SECONDS_IN_100_YEARS)

        self.TS_replacements: dict[str, str] = {}
        self.II_replacements: dict[str, str] = {}

    def anonymize_TS_value(self, element: Element):
        """Anonymize TS elements."""
        value = element.attributes["value"]
        if _is_in_replacements(value, self.TS_replacements):
            return _match_formatting(value, self.TS_replacements[value])

        known_formats = [
            "%Y",
            "%Y%m",
            "%Y%m%d",
            "%Y%m%d%H",
            "%Y%m%d%H%M",
            "%Y%m%d%H%M%S",
            "%Y%m%d%H%M%S%z",
        ]
        date_time = None
        value = element.attributes["value"]
        for fmt in known_formats:
            try:
                date_time = datetime.strptime(value, fmt)
                break
            except ValueError:
                continue

        if date_time:
            date_time = date_time - timedelta(seconds=self.time_offset)
        else:
            # if we were unable to parse the date, just use the current time
            date_time = datetime.now() - timedelta(seconds=self.time_offset)
            fmt = "%Y%m%d%H%M%S%z"

        new_value = date_time.strftime(fmt)
        self.TS_replacements[value] = new_value

        return _match_formatting(value, new_value)

    def anonymize_II_value(self, element: Element):
        """Anonymize II elements."""
        extension = element.attributes["extension"]
        if _is_in_replacements(extension, self.II_replacements):
            return _match_formatting(extension, self.II_replacements[extension])
        replacement = ""
        for i, char in enumerate(extension):
            if len(extension) > 3 and i < 3 and (char.isdigit() or char.isalpha()):
                replacement += "X"
            elif char.isdigit():
                replacement += str(randint(0, 9))
            elif char.isalpha() and char.islower():
                replacement += choice(ascii_lowercase)
            elif char.isalpha() and char.isupper():
                replacement += choice(ascii_uppercase)
            else:
                replacement += char

        self.II_replacements[extension] = replacement

        return _match_formatting(extension, replacement)
