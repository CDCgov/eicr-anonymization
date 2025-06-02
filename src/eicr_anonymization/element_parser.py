"""Parse for stepping through XML elements of a CDA document to collect sensitive elements and safe text."""  # noqa: E501

import yaml
from lxml.etree import _Element


def track_path(element_type: str):
    """Track the current path in the XML document."""

    def decorator_track_path(func):
        def wrapper(self: "Parser", element: _Element, skip_children: list[str] | None = None):
            """Track the path."""
            root_tag = str(element.tag).removeprefix("{urn:hl7-org:v3}")

            self.current_type_path.append(element_type)
            self.current_tag_path.append(root_tag)

            if (
                self.config.get("skip")
                and self.config["skip"].get("by_type")
                and element_type in self.config["skip"]["by_type"]
            ):
                skip_children = self.config["skip"]["by_type"][element_type]
                if skip_children is None:
                    self.current_type_path.pop()
                    self.current_tag_path.pop()
                    return
                else:
                    try:
                        return func(self, element, skip_children)
                    finally:
                        self.current_type_path.pop()
                        self.current_tag_path.pop()
            elif (
                self.config.get("skip")
                and self.config["skip"].get("by_path")
                and "/".join(self.current_tag_path) in self.config["skip"]["by_path"]
            ):
                self.current_type_path.pop()
                self.current_tag_path.pop()
                return
            try:
                return func(self, element)
            finally:
                self.current_type_path.pop()
                self.current_tag_path.pop()

        return wrapper

    return decorator_track_path


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
        type_path: list[str] | None = None,
        tag_path: list[str] | None = None,
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

        if tag_path and type_path:
            debug_path = []
            for type, tag in zip(type_path or [], tag_path or [], strict=True):
                debug_path.append(f"{type}:{tag}")
            self.debug_path = "/".join(debug_path)
        else:
            self.debug_path = None

    def __repr__(self) -> str:
        """Get a string representation of the tag."""
        root_tag = str(self.name).removeprefix("{urn:hl7-org:v3}")
        if self.debug_path:
            repr = f"{self.line}|{self.debug_path}|<{root_tag}"
        else:
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

    def __init__(self):
        """Initialize the Parser with an empty list of sensitive elements."""
        self.sensitive_elements: list[Element] = []
        self.safe_text: set[str] = set()
        self.current_type_path: list[str] = []
        self.current_tag_path: list[str] = []

        with open("src/eicr_anonymization/config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)
        if not isinstance(self.config, dict):
            self.config = {}

        # self.child_type_mapping = {
        #     "ClinicalDocument": {
        #         "effective"
        #     }

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

    def add_sensitive_element(self, element: _Element, cda_type: str):
        """Add a sensitive element to the list."""
        self.sensitive_elements.append(
            Element(element, cda_type, self.current_type_path, self.current_tag_path)
        )

    def add_safe_text(self, text: str):
        """Add a safe text element to the list."""
        self.safe_text.add(text)

    def parse_element(self, element: _Element, element_type: str):
        """Parse an XML element."""
        element_config = self.config["sensitive_data"]["by_type"][element_type]
        element_child_types = self.config["child_type_map"][element_type]
        sensitive_children = element_config["sensitive_children"]
        sensitive_attributes = element_config["sensitive_attributes"]

        if element_config["text_content_sensitive"] and has_text(element):
            self.add_sensitive_element(element, element_type)

        if sensitive_attributes is not None:
            for attribute in element.items():
                if attribute[0] in sensitive_attributes:
                    self.add_sensitive_element(element, element_type)

        if sensitive_children is None:
            return
        for child in element:
            child_tag = str(child.tag).removeprefix("{urn:hl7-org:v3}")
            expected_child_type = element_child_types.get(child_tag)
            if isinstance(expected_child_type, str):
                child_type = expected_child_type
            elif isinstance(expected_child_type, dict):
                if "types" in expected_child_type:
                    data_type = child.get("{http://www.w3.org/2001/XMLSchema-instance}type")
                    child_type = (
                        expected_child_type["default_type"] if data_type is None else data_type
                    )
                else:
                    sub_child = next(child.iterchildren())  # There's only ever one child
                    sub_child_tag = str(sub_child.tag).removeprefix("{urn:hl7-org:v3}")
                    expected_sub_child_type = expected_child_type[sub_child_tag]

                    if sub_child_tag in [
                        sensitive_child["sensitive_children"]
                        for sensitive_child in sensitive_children
                        if isinstance(child, dict)
                    ]:
                        self.parse_element(sub_child, expected_sub_child_type)

                    continue

            else:
                continue

            if child_tag in sensitive_children:
                self.parse_element(child, child_type)
