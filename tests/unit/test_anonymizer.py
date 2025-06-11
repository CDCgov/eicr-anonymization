from lxml import etree

from eicr_anonymization.anonymizer import Anonymizer
from eicr_anonymization.element_parser import Element


def test_anonymize_streetAddressLine_value():
    """Test the anonymization of streetAddressLine values.

    This is not much of a unit test, but will at least flag if anything changes.
    """
    anonymizer = Anonymizer(reproducible=1)


    element = etree.Element("streetAddressLine")
    element.text = "123 Main St"

    parsed_element = Element(element, "ADXP")
    anonymized_value = anonymizer.anonymize_streetAddressLine_value(parsed_element)
    assert anonymized_value == "914 City St"

def test_anonymize_streetAddressLine_USPSBoxID_value():
    """Test the anonymization of USPSBoxID values.

    This is not much of a unit test, but will at least flag if anything changes.
    """
    anonymizer = Anonymizer(reproducible=1)

    element = etree.Element("streetAddressLine")
    element.text = "PO Box 123"

    parsed_element = Element(element, "ADXP")
    anonymized_value = anonymizer.anonymize_streetAddressLine_value(parsed_element)
    assert anonymized_value == "PO Box 914"
