import random
from datetime import datetime

import pytest
from freezegun import freeze_time
from lxml import etree

from eicr_anonymization.anonymizer import Anonymizer
from eicr_anonymization.element_parser import Element


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
    @pytest.mark.repeat(3)
    def test_YYYYMMDDHHmmssz(self):
        """Test that the anonymizer correctly anonymizes the effectiveTime value."""
        # Arrange
        value = "20150919161829+0000"
        obj = Anonymizer(reproducible=True)
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
        """Test that the anonymizer correctly anonymizes the effectiveTime value."""
        # Arrange
        value = "20141023"
        obj = Anonymizer(reproducible=True)
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
