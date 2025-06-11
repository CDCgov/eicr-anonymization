"""Parse for stepping through XML elements of a CDA document to collect sensitive elements and safe text."""  # noqa: E501

import yaml
from lxml.etree import _Element


def has_text(element: _Element) -> bool:
    """Check if the XML element has text content.

    Args:
        element: The XML element to check.

    Returns:
        bool: True if the element has text content, False otherwise.
    """
    return element.text is not None and element.text.strip() != ""


class Element:
    """Class representing an XML element with its attributes and text content."""

    def __init__(
        self,
        element: _Element,
        cda_type: str,
    ):
        """Initialize the Element with its attributes and text content."""
        self.name = element.tag

        self.attributes = {}
        for attribute in element.items():
            self.attributes[attribute[0]] = attribute[1]
        self.cda_type = cda_type
        self.text = element.text
        self.path = element.getroottree().getpath(element)
        self.line = element.sourceline

    def __repr__(self) -> str:
        """Get a string representation of the tag."""
        root_tag = str(self.name).removeprefix("{urn:hl7-org:v3}")
        repr = f"{self.line}|{self.cda_type}| <{root_tag}"
        for key, value in self.attributes.items():
            root_key = key.removeprefix("{http://www.w3.org/2001/XMLSchema-instance}")
            repr += f' {root_key}="{value}"'

        if self.text:
            repr += f">{self.text.strip()}</{root_tag}>"
        else:
            repr += "/>"

        return repr


class Parser:
    """Class for finding sensitive elements in an XML document."""

    def __init__(self, config: dict | None = None):
        """Initialize the Parser with an empty list of sensitive elements."""
        self.sensitive_elements: list[Element] = []
        self.safe_text: set[str] = set()

        with open("src/eicr_anonymization/schema_structure.yaml") as structure_file:
            self.structure = yaml.safe_load(structure_file)

        with open("src/eicr_anonymization/config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)

    def add_safe_text(self, text: str):
        """Add a safe text element to the list."""
        self.safe_text.add(text)

    def add_sensitive_element(self, element: _Element, cda_type: str):
        """Add a sensitive element to the list."""
        self.sensitive_elements.append(Element(element, cda_type))

    def collect_sensitive_elements_and_safe_words(self, element: _Element):
        """Find sensitive elements in the XML document.

        Args:
            element: The XML element to parse.
        """
        if element.tag == "{urn:hl7-org:v3}ClinicalDocument":
            self.parse_element(element, "ClinicalDocument")
        else:
            raise ValueError(f"Unknown root element: {element.tag}")

        return self.sensitive_elements, self.safe_text

    def parse_element(self, element: _Element, element_type: str):
        # xhtml is a special case where it is always sensitive
        if element_type == "xhtml":
            self.add_sensitive_element(element, element_type)
            return

        children_safety: dict[str, str | dict[str, str]] = self.config[element_type]["elements"]
        children_types = self.structure[element_type]["elements"]

        if self.config[element_type]["text_content"] == "SAFE" and has_text(element):
            self.add_safe_text(element.text)  # type: ignore

        self.process_attributes(element, element_type)

        for child in element:
            child_tag = str(child.tag).split("}")[-1]
            if child_tag not in children_types:
                continue
            child_structure = children_types[child_tag]
            if len(child_structure["types"]) == 1:
                child_type = child_structure["types"][0]
            else:
                type_attribute = child.get("{http://www.w3.org/2001/XMLSchema-instance}type")
                if type_attribute is not None:
                    child_type = type_attribute
                else:
                    child_type = child_structure["default_type"]

            if children_safety[child_tag] == "SAFE":
                continue
            else:
                if "attributes" in child_structure:
                    self.process_attributes(child, child_type)
                if "elements" in child_structure:
                    for subelement in child:
                        subelement_tag = str(subelement.tag).split("}")[-1]
                        if subelement_tag not in child_structure["elements"]:
                            continue
                        subelement_structure = child_structure["elements"][subelement_tag]
                        subelement_type = subelement_structure["types"][0]
                        if children_safety[child_tag]["elements"][subelement_tag] == "SAFE":
                            continue
                        else:
                            self.parse_element(subelement, subelement_type)

                    continue

                self.parse_element(child, child_type)

    def process_attributes(self, element, element_type):
        for attribute in element.items():
            attribute_name = attribute[0].split("}")[-1]
            attribute_text = attribute[1]
            if attribute_name not in self.structure[element_type]["attributes"]:
                continue  # Skip attributes not defined in the structure
            attribute_type = self.structure[element_type]["attributes"][attribute_name]
            if self.config[element_type]["attributes"][attribute_name] == "SAFE":
                if attribute_type in ["string", "code"]:
                    self.add_safe_text(attribute_text)
                else:
                    continue
            else:
                self.add_sensitive_element(element, element_type)
