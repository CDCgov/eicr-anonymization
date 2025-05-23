import pytest
from lxml import etree

from eicr_anonymization.anonymize_eicr import anonymize_eicr_file
from eicr_anonymization.anonymizer import Anonymizer


def test_anonymize_eicr_file_empty_file():
    """Test the anonymization of an empty EICR file.

    If the file is empty it should raise an etree.XMLSyntaxError.
    """
    anonymizer = Anonymizer(seed=1)
    xml_file = "tests/unit/test_data/empty.xml"
    with pytest.raises(etree.XMLSyntaxError):
        anonymize_eicr_file(xml_file, anonymizer, debug=True)
