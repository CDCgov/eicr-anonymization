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


def anonymize_eicr_file(xml_file: str, anonymizer: Anonymizer, debug: bool = False) -> None:
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

    debug_output: list[tuple[Element, Element | str]] = []
    addresses = set()

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
            case "ADXP":
                match element.name:
                    case "{urn:hl7-org:v3}city":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "city")
                        debug_output.append((element, Element(match, "ADXP")))
                    case "{urn:hl7-org:v3}streetAddressLine":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.anonymize_streetAddressLine_value(element)
                        debug_output.append((element, Element(match, "ADXP")))
                    case "{urn:hl7-org:v3}country":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "country")
                        debug_output.append((element, Element(match, "ADXP")))
                    case _:
                        match = _find_element(root, element.path)
                        match.text = "REMOVED"
                        debug_output.append((element, Element(match, "ADXP")))
            case "xhtml":
                match = _find_element(root, element.path)
                for child in match:
                    match.remove(child)
                match.text = "REMOVED"
                debug_output.append((element, Element(match, "xhtml")))
            case _:
                if element.attributes.get("value") is not None:
                    match = _find_element(root, element.path)
                    match.attrib["value"] = "REMOVED"
                if element.text is not None:
                    match = _find_element(root, element.path)
                    match.text = "REMOVED"
                debug_output.append((element, Element(match, element.cda_type)))

    print(
        tabulate(
            sorted(debug_output, key=lambda x: (x[0].name, x[0].cda_type, x[0].text)),
            headers=("Orginal", "Replacement"),
            tablefmt="fancy_outline",
        )
    )

    # Save the anonymized XML file
    anonymized_file = os.path.join(
        os.path.dirname(xml_file),
        f"{os.path.basename(xml_file)}.anonymized.xml",
    )

    tree.write(anonymized_file)


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
    anonymizer = Anonymizer()
    for xml_file in xml_files:
        anonymize_eicr_file(xml_file, anonymizer, debug=args.debug)
