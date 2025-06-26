"""Main module for the EICR anonymization tool."""

import glob
import logging
import os
from argparse import Namespace

from lxml import etree
from lxml.etree import _Element, _ElementTree
from tabulate import tabulate

from eicr_anonymization.anonymizer import Anonymizer, DebugOptions
from eicr_anonymization.element_parser import Element, Parser

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
        print(f"Deleted previous anonymized file: {output_file}.anonymized.xml")


def xml_tree_to_str(tree: _ElementTree) -> str:
    """
    Generate string representation of XML element.

    Args:
        tree: XML Element tree to be formatted
    """
    return etree.tostring(tree, pretty_print=True, encoding="unicode")


def anonymize_eicr_file(
    xml_file: str, anonymizer: Anonymizer, parser: Parser, show_debug_info: bool = False
) -> _ElementTree:
    """
    Anonymize a single EICR XML file.

    Args:
        xml_file: Path to the XML file to anonymize
        anonymizer: Anonymizes the data
        debug: Flag to enable debug output

    """
    # Parse the XML file
    # This will raise an error if the file is empty.
    # Perhaps later we can handle this more gracefully.
    tree = etree.parse(xml_file, None)
    root = tree.getroot()

    # Get the first element and pass it into th elementProcessor
    first_element = next(root.iter())

    sensitive_elements, safe_words = parser.collect_sensitive_elements_and_safe_words(first_element)

    debug_output: list[tuple[Element, Element | str]] = []

    for element in sensitive_elements:
        match element.cda_type:
            case "TS" | "IVL_TS" | "PIVL_TS" | "IVXB_TS" | "SXCM_TS":
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
                    case "{urn:hl7-org:v3}county":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "county")
                        debug_output.append((element, Element(match, "ADXP")))
                    case "{urn:hl7-org:v3}postalCode":
                        match = _find_element(root, element.path)
                        if element.text is not None:
                            match.text = anonymizer.replace_with_like_chars(
                                element.text, "postalCode"
                            )
                            debug_output.append((element, Element(match, "ADXP")))
                    case "{urn:hl7-org:v3}state":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "state")
                        debug_output.append((element, Element(match, "ADXP")))
                    case _:
                        match = _find_element(root, element.path)
                        match.text = "REMOVED"
                        debug_output.append((element, Element(match, "ADXP")))
            case "ENXP":
                match element.name:
                    case "{urn:hl7-org:v3}given":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "given")
                        debug_output.append((element, Element(match, "ENXP")))
                    case "{urn:hl7-org:v3}family":
                        match = _find_element(root, element.path)
                        match.text = anonymizer.replace_from_pool(element.text, "family")
                        debug_output.append((element, Element(match, "ENXP")))
                    case _:
                        match = _find_element(root, element.path)
                        match.text = "REMOVED"
                        debug_output.append((element, Element(match, "ENXP")))
            case "EN" | "PN" | "ON":
                match = _find_element(root, element.path)
                match.text = anonymizer.anonymize_EN_value(element)
                debug_output.append((element, Element(match, element.cda_type)))
            case "xhtml":
                match = _find_element(root, element.path)
                anonymizer.anonymize_xhtml(match, safe_words)
            case "TEL":
                match = _find_element(root, element.path)
                value = element.attributes.get("value")
                if value is not None and not value.startswith("#"):
                    match.attrib["value"] = anonymizer.anonymize_TEL_value(element)
                debug_output.append((element, Element(match, "TEL")))
            case "ED":
                match = _find_element(root, element.path)
                match.text = anonymizer.anonymize_text(element.text, "state")
                debug_output.append((element, Element(match, "ED")))
            case _:
                if element.attributes.get("value") is not None:
                    match = _find_element(root, element.path)
                    match.attrib["value"] = anonymizer.remove_unknown_text(match.attrib["value"])
                if element.text is not None and element.text.strip() != "":
                    match = _find_element(root, element.path)
                    match.text = anonymizer.remove_unknown_text(match.text)

    print(f"Anonymized {len(sensitive_elements)} sensitive elements in file: {xml_file}")
    debug_output_table = tabulate(
        debug_output,
        headers=("Original", "Replacement"),
        tablefmt="fancy_outline",
    )

    if show_debug_info:
        print(debug_output_table)

    return tree


def save_anonymized_file(tree: _ElementTree, xml_file: str) -> None:
    """Write an anonymized XML tree to file with .anonymized appended to original file name.

    Args:
        tree: Anonymized XML tree
        xml_file: Path to the original XML file that has been anonymized

    """
    # Save the anonymized XML file
    anonymized_file = os.path.join(
        os.path.dirname(xml_file),
        f"{os.path.basename(xml_file)}.anonymized.xml",
    )

    xml_string = xml_tree_to_str(tree)

    with open(anonymized_file, "w", encoding="utf-8") as f:
        f.write(xml_string)


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
    debugOptions = None
    if args.command == "debug":
        debugOptions = DebugOptions(args.seed, args.deterministic_functions)
    anonymizer = Anonymizer(debugOptions)
    parser = Parser(custom_config_path=args.config)
    if os.path.isdir(args.input_location):
        _delete_old_anonymized_files(args.input_location)

        xml_files = glob.glob(os.path.join(args.input_location, "*.xml"))
        if not xml_files:
            print(f"No XML files found in directory: {args.input_location}")
            return
        print(f"Found {len(xml_files)} XML files in directory: {args.input_location}")
        for xml_file in xml_files:
            anonymized_file = anonymize_eicr_file(
                xml_file, anonymizer, parser, show_debug_info=args.debug
            )
            save_anonymized_file(anonymized_file, xml_file)
    elif os.path.isfile(args.input_location):
        # IF the previously anonymized file exists, delete it
        if os.path.isfile(f"{args.input_location}.anonymized.xml"):
            os.remove(f"{args.input_location}.anonymized.xml")
            print(f"Deleted previous anonymized file: {args.input_location}.anonymized.xml")
        print(f"Anonymizing file: {args.input_location}")
        anonymized_file = anonymize_eicr_file(
            args.input_location, anonymizer, parser, show_debug_info=args.debug
        )
        save_anonymized_file(anonymized_file, args.input_location)
    else:
        print(f"Input location is not a file or directory: {args.input_location}")
        return
