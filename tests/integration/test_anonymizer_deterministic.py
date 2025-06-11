from lxml import etree

from eicr_anonymization.anonymizer import Anonymizer
from eicr_anonymization.element_parser import Element


def test_anonymize_TS_value():
    """Test that the anonymizer correctly anonymizes the effectiveTime value."""
    # Arrange
    value = "20150919161829+0000"
    obj = Anonymizer(reproducible=True)
    _element = etree.Element(
        "{urn:hl7-org:v3}effectiveTime",
        attrib={
            "value": value,
        },
    )
    element = Element(_element, "TS")

    # Act
    result1 = obj.anonymize_TS_value(element)
    result2 = obj.anonymize_TS_value(element)
    # Assert
    assert result1 == result2, "Same parameters should produce same results"
