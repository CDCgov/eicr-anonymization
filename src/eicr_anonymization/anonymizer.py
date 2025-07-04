"""Anonymizer class for EICR data.

This module handles logic around replacing data with similar but fake data.
"""

import random
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from string import ascii_lowercase, ascii_uppercase
from typing import Literal, NotRequired, TypedDict

import usaddress
import yaml
from lxml.etree import _Element

from eicr_anonymization.determinism import deterministic
from eicr_anonymization.element_parser import Element

ONE_THIRD = 0.33
ONE_HALF = 0.5
TWO_THIRDS = 0.67


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
    """Normalize value by removing leading and trailing whitespace and converting to lowercase."""
    value = re.sub(r"\s+|[\.\-\(\)]", "", value)

    return value.lower()


@dataclass
class DebugOptions:
    """Dataclass for holding options for setting the random seed and making functions deterministic.

    Should not be used in production or when real sensitive data is being used.

    Args:
        seed (int): Set the random seed
        deterministic_functions (bool): If True, the same value will always be replaced with the
        same new value. This will also set the seed to its default `1`, if a seed is not provided.
    """

    seed: int | None = None
    deterministic_functions: bool = False


class Anonymizer:
    """Anonymizes the data."""

    def __init__(
        self,
        debugOptions: DebugOptions | None = None,
    ):
        """Initialize the Anonymizer class.

        Args:
            debugOptions: Options for setting the random seed and making functions deterministic.
            Should not be used in production or when real sensitive data is being used.
        """
        if debugOptions is None:
            self.is_deterministic = False
        else:
            self.is_deterministic = debugOptions.deterministic_functions
            if debugOptions.deterministic_functions is True and debugOptions.seed is None:
                self.seed = 1
                random.seed(self.seed)
            elif debugOptions.seed is not None:
                self.seed = debugOptions.seed
                random.seed(self.seed)

        SECONDS_IN_100_YEARS = int(100 * 60 * 60 * 24 * 365.25)
        # The main offset is a random number of seconds between 0 and 100 years
        self.time_offset = random.randint(0, SECONDS_IN_100_YEARS)

        self.ASSUMED_ABBR_LEN = 3
        self.NUM_X = 2

        self.data_pools = {
            "country": _read_yaml("country_names.yaml"),
            "state": _read_yaml("state_names.yaml"),
            "county": _read_yaml("county_names.yaml"),
            "city": _read_yaml("city_names.yaml"),
            "streetNameBase": _read_yaml("street_names.yaml"),
            "streetNameType": _read_yaml("street_types.yaml"),
            "family": _read_yaml("family_names.yaml"),
            "given": _read_yaml("given_names.yaml"),
        }

        self.available_options = {data_type: [] for data_type in self.data_pools}

        self.mappings: dict[str, dict[str, str]] = {
            "II": {},
            "EN": {},
            "TEL": {},
            "country": {},
            "state": {},
            "county": {},
            "city": {},
            "postalCode": {},
            "houseNumber": {},
            "streetNameBase": {},
            "streetNameType": {},
            "unitID": {},
            "AddressNumberSuffix": {},
            "given": {},
            "family": {},
            "USPSBoxGroupID": {},
            "USPSBoxID": {},
        }

        self.safe_words = {
            "",
        }

        self.safe_words.update(
            {_normalize_value(word["value"]) for word in _read_yaml("safe_words.yaml")}
        )

    @deterministic
    def anonymize_TS_value(self, element: Element):
        """Anonymize TS elements."""
        value = element.attributes["value"]
        if value is None:
            return value

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

        return _match_formatting(value, date_time.strftime(fmt))

    @deterministic
    def anonymize_II_value(self, element: Element):
        """Anonymize II elements."""
        extension = element.attributes["extension"]
        if extension is None:
            return extension

        replacement = self._get_mapping(extension, "II")
        if replacement is not None:
            return _match_formatting(extension, replacement)
        replacement = ""
        for i, char in enumerate(extension):
            if (
                len(extension) > self.NUM_X
                and i < self.NUM_X
                and (char.isdigit() or char.isalpha())
            ):
                replacement += "X"
            elif char.isdigit():
                replacement += str(random.randint(0, 9))
            elif char.isalpha() and char.islower():
                replacement += random.choice(ascii_lowercase)
            elif char.isalpha() and char.isupper():
                replacement += random.choice(ascii_uppercase)
            else:
                replacement += char

        self._set_mapping(extension, "II", replacement)

        return _match_formatting(extension, replacement)

    @deterministic
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
                    if self._get_mapping(component, "houseNumber"):
                        replacement.append(
                            _match_formatting(component, self.mappings["houseNumber"][component])
                        )
                        continue
                    replacement_AddressNumber = ""
                    for i in str(component):
                        replacement_AddressNumber += str(random.randint(0, 9)) if i.isdigit() else i
                    self._set_mapping(component, "houseNumber", replacement_AddressNumber)
                    replacement.append(_match_formatting(component, replacement_AddressNumber))
                case "AddressNumberPrefix":
                    # a modifier before an address number, e.g. 'Mile', '#'
                    replacement.append(component)
                case "AddressNumberSuffix":
                    # a modifier after an address number, e.g 'B', '1/2'
                    replacement_AddressNumberSuffix = self.replace_with_like_chars(
                        component, "AddressNumberSuffix"
                    )
                    replacement.append(replacement_AddressNumberSuffix)
                case "BuildingName":
                    replacement.append(_match_formatting(component, "Building"))
                case "CornerOf":
                    replacement.append(component)
                case "LandmarkName":
                    replacement.append(_match_formatting(component, "Landmark"))
                case "NotAddress":
                    replacement.append(component)
                case "OccupancyIdentifier":
                    # the identifier of an occupancy, often a number or letter
                    replacement_unitID = self.replace_with_like_chars(component, "unitID")
                    replacement.append(replacement_unitID)
                case "OccupancyType":
                    # a type of occupancy within a building, e.g. 'Suite', 'Apt', 'Floor'
                    replacement.append(component)
                case "PlaceName":
                    # city
                    city_replacement = self.replace_from_pool(component, "city")
                    replacement.append(city_replacement)
                case "Recipient":
                    # a non-address recipient, e.g. the name of a person/organization
                    replacement.append(_match_formatting(component, "Recipient"))
                case "StateName":
                    state_replacement = self.replace_from_pool(component, "state")
                    replacement.append(state_replacement)
                case "StreetName":
                    state_replacement = self.replace_from_pool(component, "streetNameBase")
                    replacement.append(state_replacement)
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
                    # the identifier of a USPS box group, usually a number
                    replacement_USPSBoxGroupID = self.replace_with_like_chars(
                        component, "USPSBoxGroupID"
                    )
                    replacement.append(replacement_USPSBoxGroupID)
                case "USPSBoxGroupType":
                    # a name for a group of USPS boxes, e.g. ‘RR’
                    replacement.append(component)
                case "USPSBoxID":
                    # the identifier of a USPS box, usually a number
                    replacement_USPSBoxID = self.replace_with_like_chars(component, "USPSBoxID")
                    replacement.append(replacement_USPSBoxID)
                case "USPSBoxType":
                    # a USPS box, e.g. ‘P.O. Box’
                    replacement.append(component)
                case "postalCode":
                    replacement_postalCode = self.replace_with_like_chars(component, "postalCode")
                    replacement.append(replacement_postalCode)

        return _match_formatting(value, " ".join(replacement))

    def _get_mapping(self, value: str, data_type: str):
        """Get the mapping for a value."""
        normalized = _normalize_value(value)
        if normalized in self.mappings[data_type]:
            return self.mappings[data_type][normalized]
        else:
            return None

    def _set_mapping(self, value: str, data_type: str, replacement: str):
        """Set the mapping for a value."""
        normalized = _normalize_value(value)
        self.mappings[data_type][normalized] = replacement

    @deterministic
    def replace_from_pool(self, value: str | None, data_type: str):
        """Anonymize using the pool-based replacement strategy."""
        if value is None:
            return value
        if value.isdigit() or len(value) <= self.ASSUMED_ABBR_LEN:
            return _match_formatting(value, self.replace_with_like_chars(value, data_type))
        replacement = self._get_mapping(value, data_type)
        if replacement is None:
            # Get a new replacement value
            replacement = self._get_random_option(data_type)["value"]
            # Store the mapping for future use
            self._set_mapping(value, data_type, replacement)

        return _match_formatting(value, replacement)

    @deterministic
    def replace_with_like_chars(self, value: str, data_type: str):
        """Replace each character in a string with a random character of the same type."""
        replacement = self._get_mapping(value, data_type)
        if replacement is None:
            replacement = ""
            for char in str(value):
                if char.isdigit():
                    replacement += str(random.randint(0, 9))
                elif char.isalpha() and char.islower():
                    replacement += random.choice(ascii_lowercase)
                elif char.isalpha() and char.isupper():
                    replacement += random.choice(ascii_uppercase)
                else:
                    replacement += char

            self._set_mapping(value, data_type, replacement)

        return _match_formatting(value, replacement)

    def _get_random_option(self, data_type):
        """Get a random item from the specified data type's available options."""
        options = self.available_options[data_type]
        pool = self.data_pools[data_type]

        # If options are depleted, refill from the pool and shuffle
        if not options:
            options.extend(pool.copy())
            random.shuffle(options)

        # Pop the first item
        return options.pop(0)

    @deterministic
    def anonymize_EN_value(self, element: Element):
        """Anonymize EN elements.

        https://parserator.datamade.us/probablepeople/
        """
        return self._random_corporationName(element.text)

    def _random_corporationName(self, value: str | None):
        """Generate a random corporation name."""
        if value is None:
            return value
        replacement = self._get_mapping(value, "EN")
        if replacement is not None:
            return _match_formatting(value, replacement)

        facilityTypes = [
            "Hospital",
            "Clinic",
            "Health Center",
            "Medical Center",
            "Urgent Care",
            "Laboratory",
            "Pharmacy",
            "Research Institute",
            "Health System",
        ]
        organizationTypes = ["University", "College", "School", "Academy", "Institute"]

        localitys = [
            item["value"]
            for key in ["city", "county", "state", "country"]
            for item in self.data_pools.get(key, [])
        ]

        scopes = [
            "Neighborhood",
            "Neighbourhood",
            "Regional",
        ]

        conjuctions = ["and", "&", "+"]

        form_choice = random.randint(0, 1)
        replacement = "REMOVED"
        parts = []
        match form_choice:
            case 0:
                form_choice = random.random()
                if form_choice <= ONE_THIRD:
                    parts.append(f" {random.choice(localitys)} {random.choice(organizationTypes)}")
                elif form_choice <= TWO_THIRDS:
                    parts.append(
                        f"{random.choice(organizationTypes)} of {random.choice(localitys)}"
                    )
                else:
                    parts.append(random.choice(localitys))

                if random.random() <= ONE_HALF:
                    parts.append(f"{random.choice(scopes)} {random.choice(facilityTypes)}")
                else:
                    parts.append(random.choice(facilityTypes))

                if random.random() <= ONE_HALF:
                    parts.append(f"{random.choice(conjuctions)} {random.choice(facilityTypes)}")
            case 1:
                if random.random() <= ONE_HALF:
                    parts.append(random.choice(organizationTypes))

                if random.random() <= ONE_HALF:
                    parts.append(random.choice(scopes))

                parts.append(random.choice(facilityTypes))

                if random.random() <= ONE_HALF:
                    parts.append(f"{random.choice(conjuctions)} {random.choice(facilityTypes)}")

                parts.append(f"of {random.choice(localitys)}")

        replacement = " ".join(parts)
        self._set_mapping(value, "EN", replacement)
        return _match_formatting(value, replacement)

    @deterministic
    def anonymize_TEL_value(self, element: Element):
        """Anonymize TEL elements."""
        value = element.attributes["value"]
        if value is None:
            return value

        replacement = self._get_mapping(value, "TEL")
        if replacement is not None:
            return _match_formatting(value, replacement)

        if value.startswith("mailto:"):
            replacement = self._random_email()
        elif value.startswith("tel:"):
            replacement = value
            replacement = f"tel:{self.replace_with_like_chars(value[4:], 'TEL')}"
        elif value.startswith("fax:"):
            replacement = value
            replacement = f"fax:{self.replace_with_like_chars(value[4:], 'TEL')}"
        elif value.startswith("http://"):
            replacement = self._random_web_address()
        elif value.startswith("https://"):
            replacement = self._random_web_address("https")
        else:
            replacement = "REMOVED"

        return _match_formatting(value, replacement)

    def _random_web_address(self, protocol: str = "http"):
        """Generate a random web address."""
        prefix = "".join(random.choice(ascii_lowercase) for _ in range(random.randint(0, 5)))
        if prefix != "":
            prefix += "."
        suffix = "".join(random.choice("0123456789") for _ in range(random.randint(0, 5)))
        replacement = f"{protocol}://{prefix}example{suffix}.com"
        if random.random() <= ONE_HALF:
            replacement += "/" + "".join(
                random.choice(ascii_lowercase) for _ in range(random.randint(0, 5))
            )
            replacement += random.choice(
                ["", ".pdf", ".html", ".xml", ".txt", ".jpg", ".png", ".gif", ".jpeg"]
            )
        return replacement

    def _random_email(self):
        """Generate a random email address."""
        domain = "example.com"

        name = "mailto:"

        name += "".join(random.choice(ascii_lowercase) for _ in range(random.randint(1, 5)))
        form_choice = random.random()
        if form_choice <= ONE_THIRD:
            name += "".join(random.choice(["", "_", "."]))
            name += "".join(random.choice("0123456789") for _ in range(random.randint(1, 3)))
        elif form_choice <= TWO_THIRDS:
            name += "".join(random.choice(["", "_", "."]))
            name += "".join(random.choice(ascii_lowercase) for _ in range(random.randint(1, 3)))
        return f"{name}@{domain}"

    @deterministic
    def anonymize_text(self, value: str | None, data_type: str):
        """Anonymize text elements."""
        if (
            value is None
            or value == ""
            or value.isdigit()
            or _normalize_value(value) in self.safe_words
        ):
            return value

        return "REMOVED"

    @deterministic
    def anonymize_xhtml(self, element: _Element, additional_safe_words: set[str] | None = None):
        """Anonymize xhtml elements."""
        if additional_safe_words is None:
            additional_safe_words = set()

        self.safe_words.update({_normalize_value(word) for word in additional_safe_words})

        text_value = element.text
        if text_value is not None:
            normalized_text_value = _normalize_value(text_value)
            if (
                normalized_text_value != ""
                and len(normalized_text_value) > self.ASSUMED_ABBR_LEN
                and not (
                    any(normalized_text_value in safe_word for safe_word in self.safe_words)
                    or normalized_text_value.isnumeric()
                )
            ):
                element.text = _match_formatting(text_value, "REMOVED")

        tail_value = element.tail
        if tail_value is not None:
            normalized_tail_value = _normalize_value(tail_value)
            if (
                normalized_tail_value != ""
                and len(normalized_tail_value) > self.ASSUMED_ABBR_LEN
                and not (
                    any(normalized_tail_value in safe_word for safe_word in self.safe_words)
                    or normalized_tail_value.isnumeric()
                )
            ):
                element.tail = _match_formatting(tail_value, "REMOVED")

        for child in element:
            self.anonymize_xhtml(child)

    def remove_unknown_text(self, text: str):
        """Replace text of unknown data types with "REMOVED".

        First check if text is a known value, if not, replace it with "REMOVED".
        """
        normalized_value = _normalize_value(text)
        if normalized_value in self.safe_words or normalized_value.isnumeric():
            return text
        return "REMOVED"
