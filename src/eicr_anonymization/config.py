from enum import Enum
from typing import Iterable

import yaml
from pydantic import BaseModel, RootModel, model_validator

with open("src/eicr_anonymization/cda_structure.yaml") as f:
    structure = yaml.safe_load(f)

    all_types = set(structure.keys())


class Sensitivity(Enum):
    SAFE = "SAFE"
    SENSITIVE = None


type ConfigSection = dict[str, Sensitivity]


class CustomTypeConfig(BaseModel):
    """Model for the configuration of a type in a custom configuration.

    Every field is optional, but if a field is defined, it must be of the correct type.
    """

    text_content: Sensitivity | None = None
    attributes: ConfigSection | None = None
    elements: dict[str, Sensitivity | dict[str, Sensitivity | ConfigSection]] | None = None


class CustomConfig(RootModel):
    """Model for the default configuration."""

    root: dict[str, CustomTypeConfig]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def items(self):
        return self.root.items()

    @model_validator(mode="after")
    def check_elements(self):
        """Check that all types, attributes, and elements in the configuration are known found in the structure."""
        all_types = set(structure)
        all_in_config = set(self)
        _check_unknown_items(all_in_config, all_types, "types", "custom configuration")

        for type_name, type_config in self.items():
            _check_section_partial(
                type_config.attributes,
                structure[type_name]["attributes"],
                "attributes",
                f"type '{type_name}' in custom custom configuration",
            )

            _check_section_partial(
                type_config.elements,
                structure[type_name]["elements"],
                "elements",
                f"type '{type_name}' in custom configuration",
            )

            for elem, elem_config in type_config.elements.items():
                if isinstance(elem_config, dict):
                    if "attributes" not in elem_config and "elements" not in elem_config:
                        _check_section_partial(
                            elem_config,
                            structure[type_name]["elements"][elem],
                            "sub-elements",
                            f"element '{elem}' of type '{type_name}' in custom configuration",
                        )
                        continue

                    if "attributes" in elem_config:
                        _check_section_partial(
                            elem_config["attributes"],
                            structure[type_name]["elements"][elem]["attributes"],
                            "sub-element attributes",
                            f"'{elem}' of type '{type_name}' in default configuration",
                        )
                    if "elements" in elem_config:
                        _check_section_partial(
                            elem_config["elements"],
                            structure[type_name]["elements"][elem]["elements"],
                            "sub-elements",
                            f"'{elem}' of type '{type_name}' in default configuration",
                        )


class DefaultTypeConfig(BaseModel):
    """Model for the default configuration of a type.

    This is used to define the default configuration for types in the `CustomConfig`.
    """

    text_content: Sensitivity
    attributes: ConfigSection
    elements: dict[str, Sensitivity | dict[str, Sensitivity | ConfigSection]]


class DefaultConfig(CustomConfig):
    @model_validator(mode="after")
    def check_elements(self):
        """Check that all types, attributes, and elements in the configuration are known found in the structure."""
        all_types = set(structure)
        all_in_config = set(self)
        _check_unknown_items(all_in_config, all_types, "types", "default configuration")
        _check_missing_items(all_in_config, all_types, "types", "default configuration")

        for type_name, type_config in self.items():
            _check_section_complete(
                type_config.attributes,
                structure[type_name]["attributes"],
                "attributes",
                f"type '{type_name}' in default configuration",
            )

            _check_section_complete(
                type_config.elements,
                structure[type_name]["elements"],
                "elements",
                f"type '{type_name}' in default configuration",
            )

            for elem, elem_config in type_config.elements.items():
                if isinstance(elem_config, dict):
                    if "attributes" not in elem_config and "elements" not in elem_config:
                        _check_section_complete(
                            elem_config,
                            structure[type_name]["elements"][elem],
                            "sub-elements",
                            f"element '{elem}' of type '{type_name}' in custom configuration",
                        )
                        continue

                    if "attributes" in elem_config:
                        _check_section_complete(
                            elem_config["attributes"],
                            structure[type_name]["elements"][elem]["attributes"],
                            "sub-element attributes",
                            f"'{elem}' of type '{type_name}' in default configuration",
                        )
                    if "elements" in elem_config:
                        _check_section_complete(
                            elem_config["elements"],
                            structure[type_name]["elements"][elem]["elements"],
                            "sub-elements",
                            f"'{elem}' of type '{type_name}' in default configuration",
                        )


def _check_section_partial(
    all_in_config, all_in_structure, section_name: str, context: str
) -> None:
    if all_in_config is None:
        all_in_config = set()
    _check_unknown_items(set(all_in_config), set(all_in_structure), section_name, context)


def _check_section_complete(
    all_in_config, all_in_structure, section_name: str, context: str
) -> None:
    """Check that all items in the configuration are known and raise error if not."""
    if all_in_config is None:
        all_in_config = set()
    _check_unknown_items(set(all_in_config), set(all_in_structure), section_name, context)
    _check_missing_items(set(all_in_config), set(all_in_structure), section_name, context)


def _check_unknown_items(
    all_in_config: set[str], all_in_structure: set[str], section_name: str, context: str
) -> None:
    """Check for unknown items and raise error if found."""
    unknown_items = all_in_config - all_in_structure
    if unknown_items:
        raise UnknownItem(section_name, context, unknown_items)


def _check_missing_items(
    all_in_config: set[str], all_in_structure: set[str], section_name: str, context: str
) -> None:
    """Check for missing items and raise error if found."""
    missing_items = all_in_structure - all_in_config
    if missing_items:
        raise MissingItem(section_name, context, missing_items)


class UnknownItem(Exception):
    """Exception raised when an unknown item is found in the configuration."""

    def __init__(self, section_name, context: str, items: Iterable[str]):
        super().__init__(f"Unknown {section_name} in {context}: {', '.join(items)}")


class MissingItem(Exception):
    """Exception raised when an item is missing in the configuration."""

    def __init__(self, section_name, context: str, items: Iterable[str]):
        super().__init__(f"Missing {section_name} in {context}: {', '.join(items)}")
