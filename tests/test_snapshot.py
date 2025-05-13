import pytest

from lxml import etree
from pathlib import Path

from eicr_anonymization.anonimizer import Anonymizer
from eicr_anonymization.anonymize_eicr import anonymize_eicr_file


@pytest.mark.parametrize('dir', list(Path('tests/test_data').iterdir()))
def test_snapshot(dir, snapshot):
    """

    """
    xml_files = list(dir.glob('*.xml'))

    anonymizer = Anonymizer(seed=1)

    for xml_file in xml_files:
        # Output anonmyized XML tree
        actual = anonymize_eicr_file(xml_file, anonymizer)
        actual_xml = etree.tostring(actual, pretty_print=True, encoding="unicode")

        snapshot.snapshot_dir = f"tests/snapshots/{dir.name}"
        snapshot.assert_match(actual_xml, f"{xml_file.stem}_anonymized_snapshot.xml")