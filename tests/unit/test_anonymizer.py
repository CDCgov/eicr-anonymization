"""Unit tests for the Anonymizer class."""

import random
from datetime import datetime

import pytest
from freezegun import freeze_time
from lxml import etree

from eicr_anonymization.anonymizer import Anonymizer, DebugOptions
from eicr_anonymization.element_parser import Element

debugOptions = DebugOptions(seed=1)


@pytest.fixture
def set_random_seed(request):
    """Set up a random seed for reproducibility.

    This fixture ensures that the random seed is set to a fixed value for the first iteration of
    each test function. This ensures that we get deterministic results regardless of the order
    in which the tests are run.
    """
    callspec = getattr(request.node, "callspec", None)
    repeat_iteration = callspec.params.get("__pytest_repeat_step_number", 0) if callspec else 0
    random.seed(repeat_iteration)


@freeze_time("2025-01-10 09:30:30")
class TestAnonymizeTSValue:
    """Unit tests for the anonymize_TS_value method."""

    @pytest.mark.repeat(3)
    def test_YYYYMMDDHHmmssz(self):
        """Test `anonymize_TS_value` for a value with the format `YYYYMMDDHHmmssz`."""
        # Arrange
        value = "20150919161829+0000"
        obj = Anonymizer(debugOptions)
        _element = etree.Element(
            "{urn:hl7-org:v3}effectiveTime",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "IVL_TS",
                "value": value,
            },
        )
        element = Element(_element, "TS")

        # Act
        result = obj.anonymize_TS_value(element)
        # Assert
        assert len(result) == len(value), (
            "Anonymized timestamp value should have the same length as the original value"
        )
        try:
            datetime.strptime(result, "%Y%m%d%H%M%S%z")
        except ValueError:
            pytest.fail(f"Date '{result}' does not match expected format 'YYYYMMDDHHmmssz'")

    @pytest.mark.repeat(3)
    def test_YYYYMMDD(self):
        """Test `anonymize_TS_value` for a value with the format `YYYMMDD`."""
        # Arrange
        value = "20141023"
        obj = Anonymizer(debugOptions)
        _element = etree.Element(
            "{urn:hl7-org:v3}effectiveTime",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "IVL_TS",
                "value": value,
            },
        )
        element = Element(_element, "TS")

        # Act
        result = obj.anonymize_TS_value(element)
        # Assert
        assert len(result) == len(value), (
            "Anonymized timestamp value should have the same length as the original value"
        )
        try:
            datetime.strptime(result, "%Y%m%d")
        except ValueError:
            pytest.fail(f"Date '{result}' does not match expected format 'YYYYMMDD'")


def test_anonymize_streetAddressLine_value():
    """Test the anonymization of streetAddressLine values.

    For street address we want the replacement value to follow the following rules:
    - Same number of digits in house number
    - Same street type ending.
    """
    anonymizer = Anonymizer(debugOptions)

    element = etree.Element("streetAddressLine")
    house_number = "123"
    street_name = "Main"
    street_type = "St"
    element.text = " ".join([house_number, street_name, street_type])

    parsed_element = Element(element, "ADXP")
    anonymized_value = anonymizer.anonymize_streetAddressLine_value(parsed_element)

    if anonymized_value is None:
        pytest.fail("Anonymized value should not be None")
    anonymized_parts = anonymized_value.split(" ")
    anonymized_house_number = anonymized_parts[0]
    anonymized_street_name = " ".join(anonymized_parts[1:-1])
    anonymized_street_type = anonymized_parts[-1]

    assert anonymized_house_number.isdigit(), "House number should be numeric"
    assert len(anonymized_house_number) == len(house_number), (
        "House number should have the same number of digits"
    )

    assert anonymized_street_name != street_name, "Street name should be different"
    assert anonymized_street_type == street_type, "Street type should remain the same"


def test_anonymize_streetAddressLine_USPSBoxID_value():
    """Test the anonymization of USPSBoxID values.

    For USPS boxes we want the replacement value to follow the following rules:
    - Only the number should be different.
    - The number should have the same number of digits.
    """
    anonymizer = Anonymizer(debugOptions)

    element = etree.Element("streetAddressLine")
    po_box_prefix = "PO Box"
    po_box_number = "123"
    element.text = f"{po_box_prefix} {po_box_number}"

    parsed_element = Element(element, "ADXP")
    anonymized_value = anonymizer.anonymize_streetAddressLine_value(parsed_element)
    if anonymized_value is None:
        pytest.fail("Anonymized value should not be None")

    anonymized_parts = anonymized_value.split(" ")
    anonymized_prefix = " ".join(anonymized_parts[0:-1])
    assert anonymized_prefix == po_box_prefix, "PO Box prefix should remain the same"
    anonymized_po_box_number = anonymized_parts[-1]
    assert anonymized_po_box_number.isdigit(), "PO Box number should be numeric"
    assert len(anonymized_po_box_number) == len(po_box_number), (
        "PO Box number should have the same number of digits"
    )
