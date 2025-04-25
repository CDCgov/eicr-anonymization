from datetime import datetime, timedelta
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase
from typing import Literal, NotRequired, TypedDict

import usaddress
import yaml

from eicr_anonymization.element_parser import Element


class ReplacementType(TypedDict):
    """Type definition for a replacement."""

    value: str
    abbreviation_only: NotRequired[Literal[True]]
    abbreviations: NotRequired[list[str]]
    qualifier: NotRequired[str]


def _read_yaml(file_name: str) -> list[ReplacementType]:
    """Read a YAML file and return its contents as a list of strings."""
    with open("src/eicr_anonymization/star-wars-data/" + file_name) as file:
        return yaml.safe_load(file)


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
    return any(_compare_normalized_values(value, replacement) for replacement in replacements)


def _replace_each_char_with_like(string: str):
    """Replace each character in a string with a random character of the same type."""
    new_string = ""
    for char in str(string):
        if char.isdigit():
            new_string += str(randint(0, 9))
        elif char.isalpha() and char.islower():
            new_string += choice(ascii_lowercase)
        elif char.isalpha() and char.isupper():
            new_string += choice(ascii_uppercase)
        else:
            new_string += char
    return new_string


class Anonymizer:
    """Anonymizes the data."""

    def __init__(self):
        """Initialize the Anonymizer class."""
        SECONDS_IN_100_YEARS = int(100 * 60 * 60 * 24 * 365.25)
        # The main offset is a random number of seconds between 0 and 100 years
        self.time_offset = randint(0, SECONDS_IN_100_YEARS)

        self.TS_replacements: dict[str, str] = {}
        self.II_replacements: dict[str, str] = {}
        self.addressNumber_replacements: dict[str, str] = {}
        self.addressNumberSuffix_replacements: dict[str, str] = {}
        self.occupancyIdentifier_replacements: dict[str, str] = {}
        self.placeName_replacements: dict[str, str] = {}
        self.stateName_replacements: dict[str, str] = {}
        self.streetName_replacements: dict[str, str] = {}
        self.uSPSBoxGroupID_replacements: dict[str, str] = {}
        self.uSPSBoxID_replacements: dict[str, str] = {}
        self.zipCode_replacements: dict[str, str] = {}

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

    def anonymize_streetAddressLine_value(self, element: Element):
        """Anonymize streetAddressLine elements.

        https://parserator.datamade.us/api-docs/#accordion-api-usaddress
        """
        value = element.text

        if value is None:
            return value

        parsed_address = usaddress.parse(value)

        replacement = []

        for component, component_type in parsed_address:
            match component_type:
                case "AddressNumber":
                    if _is_in_replacements(component, self.addressNumber_replacements):
                        replacement.append(
                            _match_formatting(component, self.addressNumber_replacements[component])
                        )
                        continue
                    replacement_AddressNumber = ""
                    for i in str(component):
                        replacement_AddressNumber += str(randint(0, 9)) if i.isdigit() else i
                    self.addressNumber_replacements[component] = replacement_AddressNumber
                    replacement.append(_match_formatting(component, replacement_AddressNumber))
                case "AddressNumberPrefix":
                    # a modifier before an address number, e.g. 'Mile', '#'
                    replacement.append(component)
                case "AddressNumberSuffix":
                    if _is_in_replacements(component, self.addressNumberSuffix_replacements):
                        replacement.append(
                            _match_formatting(
                                component, self.addressNumberSuffix_replacements[component]
                            )
                        )
                        continue
                    replacement_value = _replace_each_char_with_like(component)
                    self.addressNumberSuffix_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "BuildingName":
                    replacement.append(_match_formatting(component, "Building"))
                case "CornerOf":
                    replacement.append(component)
                case "LandmarkName":
                    replacement.append(_match_formatting(component, "Landmark"))
                case "NotAddress":
                    replacement.append(component)
                case "OccupancyIdentifier":
                    if _is_in_replacements(component, self.occupancyIdentifier_replacements):
                        replacement.append(
                            _match_formatting(
                                component, self.occupancyIdentifier_replacements[component]
                            )
                        )
                        continue
                    replacement_value = _replace_each_char_with_like(component)
                    self.occupancyIdentifier_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "OccupancyType":
                    # a type of occupancy within a building, e.g. 'Suite', 'Apt', 'Floor'
                    replacement.append(component)
                case "PlaceName":
                    # city
                    if _is_in_replacements(component, self.placeName_replacements):
                        replacement.append(
                            _match_formatting(component, self.placeName_replacements[component])
                        )
                        continue
                    replacement_value = choice(_read_yaml("city_names.yaml"))["value"]
                    self.placeName_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "Recipient":
                    # a non-address recipient, e.g. the name of a person/organization
                    replacement.append(_match_formatting(component, "Recipient"))
                case "StateName":
                    if _is_in_replacements(component, self.stateName_replacements):
                        replacement.append(
                            _match_formatting(component, self.stateName_replacements[component])
                        )
                        continue
                    replacement_value = choice(_read_yaml("state_names.yaml"))["value"]
                    self.stateName_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "StreetName":
                    if _is_in_replacements(component, self.streetName_replacements):
                        replacement.append(
                            _match_formatting(component, self.streetName_replacements[component])
                        )
                        continue
                    replacement_value = choice(_read_yaml("street_names.yaml"))["value"]
                    self.streetName_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "StreetNamePostDirectional":
                    replacement.append(component)
                case "StreetNamePostModifier":
                    replacement.append(component)
                case "StreetNamePostType":
                    replacement.append(component)
                case "StreetNamePreDirectional":
                    replacement.append(component)
                case "StreetNamePreModifier":
                    replacement.append(component)
                case "StreetNamePreType":
                    replacement.append(component)
                case "SubaddressIdentifier":
                    # the name/identifier of a subaddress component
                    replacement.append(_match_formatting(component, "SubaddressIdentifier"))
                case "SubaddressType":
                    replacement.append(component)
                case "USPSBoxGroupID":
                    if _is_in_replacements(component, self.uSPSBoxGroupID_replacements):
                        replacement.append(
                            _match_formatting(
                                component, self.uSPSBoxGroupID_replacements[component]
                            )
                        )
                        continue
                    replacement_value = _replace_each_char_with_like(component)
                    self.uSPSBoxGroupID_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "USPSBoxGroupType":
                    replacement.append(component)
                case "USPSBoxID":
                    if _is_in_replacements(component, self.uSPSBoxID_replacements):
                        replacement.append(
                            _match_formatting(component, self.uSPSBoxID_replacements[component])
                        )
                        continue
                    replacement_value = _replace_each_char_with_like(component)
                    self.uSPSBoxID_replacements[component] = replacement_value
                    replacement.append(_match_formatting(component, replacement_value))
                case "USPSBoxType":
                    replacement.append(component)
                case "ZipCode":
                    if _is_in_replacements(component, self.zipCode_replacements):
                        replacement.append(
                            _match_formatting(component, self.zipCode_replacements[component])
                        )
                        continue
                    replacement_ZipCode = ""
                    for i in str(component):
                        replacement_ZipCode = str(randint(0, 9)) if i.isdigit() else i
                    self.zipCode_replacements[component] = replacement_ZipCode
                    replacement.append(_match_formatting(component, replacement_ZipCode))

        return _match_formatting(value, " ".join(replacement))

    def anonymize_city_value(self, element: Element):
        """Anonymize city elements."""
        value = element.text
        if value is None:
            return value
        if _is_in_replacements(value, self.placeName_replacements):
            return _match_formatting(value, self.placeName_replacements[value])
        replacement = choice(_read_yaml("city_names.yaml"))["value"]
        if _already_picked(replacement, self.placeName_replacements):
            replacement = _replace_each_char_with_like(replacement)
        self.placeName_replacements[value] = replacement
        return _match_formatting(value, replacement)
