"""Snapshot tests for the output of anonymize_eicr_file function.

There are two snapshot tests, one for the full anonymization and one for the light configuration.
"""

from itertools import product
from pathlib import Path

import pytest
from freezegun import freeze_time

from eicr_anonymization.anonymize_eicr import anonymize_eicr_file, xml_tree_to_str
from eicr_anonymization.anonymizer import Anonymizer, DebugOptions
from eicr_anonymization.element_parser import Parser

xml_files = list(Path("tests/test_data").rglob("*.xml"))


@freeze_time("2025-01-10 09:30:30")
@pytest.mark.parametrize(
    ("xml_file", "config"),
    list(product(xml_files, [(False, "full"), (True, "patient_only")])),
)
def test_snapshot(xml_file, config, snapshot):
    """
    Run snapshot tests.

    Args:
        xml_file (str): Path to XML file to be anonymized

    """
    anonymizer = Anonymizer(DebugOptions(deterministic_functions=True))
    dir = xml_file.parent

    # Output anonymized XML tree
    actual = anonymize_eicr_file(xml_file, anonymizer, Parser(patient_only=config[0]))
    actual_xml = xml_tree_to_str(actual)

    # Snapshot return value
    snapshot.snapshot_dir = f"tests/snapshots/{config[1]}/{dir.name}"
    snapshot.assert_match(actual_xml, f"{xml_file.stem}_anonymized_snapshot.xml")
