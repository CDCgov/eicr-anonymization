"""Main module for the EICR anonymization tool."""

import glob
import logging
import os
import sys
from argparse import Namespace
from random import randint

from lxml import etree
from lxml.etree import _Element
from tabulate import tabulate

from eicr_anonymization.anonimizer import Anonymizer
from eicr_anonymization.element_parser import Element, Parser
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
    # with open(xml_file) as f:
    #     xml_content = f.read()
    # object = xmltodict.parse(xml_content)

    # with open("initial_output.json", "w") as f:
    #     json.dump(object,f, indent=2)

    # with open("initial_output.xml", "w") as f:
    #     f.write(xmltodict.unparse(object, pretty=True))

    # Parse the XML file
    tree = etree.parse(xml_file, None)
    root = tree.getroot()

    # Get the first element and pass it into th elementProcessor
    first_element = next(root.iter())

    parser = Parser()

    sensitive_elements = parser.find_sensitive_elements(first_element)

    anonymizer = Anonymizer()

    debug_output = []

    for element in sensitive_elements:
        match element.cda_type:
            case "TS":
                match = _find_element(root, element.path)
                match.attrib["value"] = anonymizer.anonymize_TS_value(element)
                debug_output.append((element, Element(match, "TS")))
            case "II":
                match = _find_element(root, element.path)
                match.attrib["extension"] = anonymizer.anonymize_II_value(element)
                debug_output.append((element, Element(match, "II")))
            case _:
                debug_output.append((element, ""))

    print(
        tabulate(
            debug_output,
            headers=("Orginal", "Replacement"),
            tablefmt="fancy_outline",
        )
    )


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


def _find_element(root: _Element, path: str):
    """Find all elements for a given path with the HL7 namespace in an EICR XML file.

    Args:
        root: Root XML element to search
        path: XPath query to find elements

    Returns:
        List of matching XML elements

    """
    return root.xpath(path, namespaces=NAMESPACES)[0]


def anonymize(args: Namespace) -> None:
    """Run the EICR anonymization process."""
    _delete_old_anonymized_files(args.input_location)

    xml_files = glob.glob(os.path.join(args.input_location, "*.xml"))
    for xml_file in xml_files:
        anonymize_eicr_file(xml_file, debug=args.debug)
