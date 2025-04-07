"""Main module for the EICR anonymization tool."""

import glob
import logging
import os
from argparse import Namespace

from lxml import etree
from lxml.etree import Element
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


def _find_elements(root: Element, path: str) -> list[Element]:
    """Find all elements for a given path with the HL7 namespace in an EICR XML file.

    Args:
        root: Root XML element to search
        path: XPath query to find elements

    Returns:
        List of matching XML elements

    """
    return root.xpath(path, namespaces=NAMESPACES)


def _should_anonymize_element(element: Element, tag: Tag) -> bool:
    """Determine if an XML element should be anonymized.

    Args:
        element: XML element to check
        tag: Tag associated with the element

    Returns:
        Boolean indicating if the element should be anonymized

    """
    text_is_nonempty = bool(element.text and element.text.strip())
    attr_is_sensitive = hasattr(tag, "sensitive_attr") and any(
        attr in element.attrib for attr in tag.sensitive_attr
    )
    return text_is_nonempty or attr_is_sensitive


def _build_xpath_query(instance: Tag) -> str:
    """Construct an XPath query to find a specific XML element.

    Args:
        instance: Tag instance to find

    Returns:
        Constructed XPath query string

    """
    xpath_parts = [f".//ns:{instance.name}"]

    if instance.text:
        xpath_parts.append(f"[text()='{instance.text}']")

    if instance.attributes:
        for attr_name, attr_value in instance.attributes.items():
            xpath_parts.append(f'[@{attr_name}="{attr_value}"]')
    else:
        xpath_parts.append("[not(@*)]")

    return "".join(xpath_parts)


def _collect_sensitive_tag_groups(root: Element) -> NormalizedTagGroups:
    """Collect sensitive tag groups from the XML root.

    Args:
        root: Root XML element to search

    Returns:
        NormalizedTagGroups containing sensitive tags

    """
    sensitive_tag_groups = NormalizedTagGroups()
    tag_registry = Tag.get_registry().values()

    for tag in tag_registry:
        elements = _find_elements(root, f".//ns:{tag.name}")
        for element in elements:
            if _should_anonymize_element(element, tag):
                tag_instance = tag(
                    text=element.text,
                    attributes=dict(element.attrib),
                )
                sensitive_tag_groups.add(tag_instance)

    return sensitive_tag_groups


def _replace_sensitive_information(
    root: Element, sensitive_tag_groups: NormalizedTagGroups
) -> list[tuple[Tag, Tag]]:
    """Replace sensitive information in the XML root.

    Args:
        root: Root XML element to modify
        sensitive_tag_groups: Collected sensitive tag groups

    Returns:
        List of debug output containing original and replacement tags

    """
    debug_output = []

    for tag_group in sensitive_tag_groups:
        replacement_mapping = tag_group.get_replacement_mapping()

        for instance in tag_group:
            replacement = replacement_mapping[instance]
            xpath = _build_xpath_query(instance)

            matches = _find_elements(root, xpath)

            for match in matches:
                # Replace text if applicable
                if instance.text:
                    match.text = replacement.text

                # Replace attributes
                for attr, new_val in replacement.attributes.items():
                    if attr in match.attrib:
                        match.attrib[attr] = new_val

            debug_output.append([instance, replacement])

    return debug_output


def anonymize_eicr_file(xml_file: str, debug: bool = False) -> None:
    """Anonymize a single EICR XML file.

    Args:
        xml_file: Path to the XML file to anonymize
        debug: Flag to enable debug output

    """
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Collect sensitive tags
    sensitive_tag_groups = _collect_sensitive_tag_groups(root)

    # Replace sensitive information
    debug_output = _replace_sensitive_information(root, sensitive_tag_groups)

    # Write anonymized file
    tree.write(f"{xml_file}.anonymized.xml")

    # Print debug information if enabled
    if debug:
        _print_debug(debug_output)


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
