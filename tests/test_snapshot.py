from pathlib import Path

import pytest
from freezegun import freeze_time

from eicr_anonymization.anonymize_eicr import anonymize_eicr_file, xml_tree_to_str
from eicr_anonymization.anonymizer import Anonymizer


@freeze_time('2025-01-10 09:30:30')
@pytest.mark.parametrize('xml_file', list(Path('tests/test_data').rglob('*.xml')))
def test_snapshot(xml_file, snapshot):
    """
    Run snapshot tests.

    Args:
        xml_file (str): Path to XML file to be anonymized

    """
    anonymizer = Anonymizer(seed=1)
    dir = xml_file.parent

    # Output anonmyized XML tree
    actual = anonymize_eicr_file(xml_file, anonymizer)
    actual_xml = xml_tree_to_str(actual)

    # Snapshot return value
    snapshot.snapshot_dir = f"tests/snapshots/{dir.name}"
    snapshot.assert_match(actual_xml, f"{xml_file.stem}_anonymized_snapshot.xml")