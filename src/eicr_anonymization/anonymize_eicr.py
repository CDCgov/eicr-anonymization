"""Main module for the EICR anonymization tool."""

import glob
import logging
import os
from argparse import Namespace

from lxml import etree
from tabulate import tabulate
from tqdm import tqdm

from eicr_anonymization.data_cache import NormalizedTagGroups
from eicr_anonymization.tags.Tag import Tag

logger = logging.getLogger(__name__)

NAMESPACE = "urn:hl7-org:v3"
NAMESPACES = {"ns": NAMESPACE}


def _delete_old_anonymized_files(input_location: str) -> None:
    """Remove previously anonymized XML files from the input location.

    Args:
        input_location: Directory path containing XML files

    """
    previous_output_files = glob.glob(os.path.join(input_location, "*.anonymized.xml"))
    for output_file in previous_output_files:
        os.remove(output_file)



def anonymize_eicr_file(xml_file: str, debug: bool = False) -> None:
    """Anonymize a single EICR XML file.

    Args:
        xml_file: Path to the XML file to anonymize
        debug: Flag to enable debug output

    """
    # Parse the XML file
    tree = etree.parse(xml_file, None)
    root = tree.getroot()

    # step through the


def _print_debug(debug_output: list[tuple[Tag, Tag]]) -> None:
    """Print debug information for each replacement made.

    Args:
        debug_output: List of original and replacement tag instances

    """
    print(
        tabulate(
            debug_output,
            headers=["Original", "Replacement"],
            tablefmt="fancy_outline",
        )
    )


def anonymize(args: Namespace) -> None:
    """Run the EICR anonymization process."""
    _delete_old_anonymized_files(args.input_location)

    xml_files = glob.glob(os.path.join(args.input_location, "*.xml"))
    for xml_file in tqdm(xml_files, desc="Anonymizing eICR files"):
        anonymize_eicr_file(xml_file, debug=args.debug)
