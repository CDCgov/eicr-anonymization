from lxml import etree

from eicr_anonymization.anonymizer import Anonymizer
from eicr_anonymization.element_parser import Element


def test_anonymize_TS_value():
    """Test that the anonymizer correctly anonymizes the effectiveTime value.

    Time values are actually a special case because the offset is randomized on initialization.
    Therefore this function should always return the same value for the same input regardless of
    `deterministic_functions` setting. Leaving this test for completeness.
    """
    # Arrange
    value = "20150919161829+0000"
    obj = Anonymizer(deterministic_functions=True)
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


def test_determinism():
    """Test that the anonymizer's deterministic functions produce consistent results."""
    # Arrange
    anonymizer_1 = Anonymizer(deterministic_functions=True)
    anonymizer_2 = Anonymizer(deterministic_functions=True)
    anonymizer_3 = Anonymizer(deterministic_functions=True)

    id_element_1 = Element(
        etree.Element(
            "{urn:hl7-org:v3}id", attrib={"root": "test.id.123", "extension": "1234567890"}
        ),
        "II",
    )

    id_element_1_2 = Element(
        etree.Element(
            "{urn:hl7-org:v3}id", attrib={"root": "test.id.123", "extension": "1234567890"}
        ),
        "II",
    )

    id_element_2 = Element(
        etree.Element(
            "{urn:hl7-org:v3}id", attrib={"root": "different.test.id.987", "extension": "011235813"}
        ),
        "II",
    )

    # Act
    id_result_1_1 = anonymizer_1.anonymize_II_value(id_element_1)
    id_result_2_1 = anonymizer_1.anonymize_II_value(id_element_2)

    id_result_2_2 = anonymizer_2.anonymize_II_value(id_element_2)
    id_result_1_2 = anonymizer_2.anonymize_II_value(id_element_1)

    id_result_1_3 = anonymizer_3.anonymize_II_value(id_element_1_2)

    # Assert
    assert id_result_1_1 == id_result_1_2 == id_result_1_3, (
        "Anonymizers should produce the same result for the same input"
    )
    assert id_result_2_1 == id_result_2_2, (
        "Anonymizers should produce the same result for the same input"
    )

    assert id_result_1_1 != id_result_2_1, (
        "Anonymizer 1 and 2 should produce different results for different inputs"
    )
    assert id_result_1_2 != id_result_2_2, (
        "Anonymizer 1 and 2 should produce different results for different inputs"
    )


def test_nondeterminism():
    """Test that the anonymizer's deterministic functions produce consistent results."""
    # Arrange
    anonymizer_1 = Anonymizer(reproducible=True)
    anonymizer_2 = Anonymizer(reproducible=True)

    id_element_1 = Element(
        etree.Element(
            "{urn:hl7-org:v3}id", attrib={"root": "test.id.123", "extension": "1234567890"}
        ),
        "II",
    )

    id_element_2 = Element(
        etree.Element(
            "{urn:hl7-org:v3}id", attrib={"root": "different.test.id.987", "extension": "011235813"}
        ),
        "II",
    )

    # Act
    id_result_1_1 = anonymizer_1.anonymize_II_value(id_element_1)
    id_result_2_1 = anonymizer_1.anonymize_II_value(id_element_2)

    id_result_2_2 = anonymizer_2.anonymize_II_value(id_element_2)
    id_result_1_2 = anonymizer_2.anonymize_II_value(id_element_1)

    # Assert
    assert id_result_1_1 != id_result_1_2, (
        "Anonymizer 1 and 2 should produce different results for the same input"
    )
    assert id_result_2_1 != id_result_2_2, (
        "Anonymizer 1 and 2 should produce different results for the same input"
    )

    assert id_result_1_1 != id_result_2_1, (
        "The Anonymizer should produce different results for different inputs"
    )
    assert id_result_1_2 != id_result_2_2, (
        "The Anonymizer should produce different results for different inputs"
    )
