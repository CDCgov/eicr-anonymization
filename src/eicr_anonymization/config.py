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


class CustomTypeConfig(BaseModel):
    """Model for the configuration of a type in a custom configuration.

    Every field is optional, but if a field is defined, it must be of the correct type.
    """

    text_content: Sensitivity | None = None
    attributes: dict[str, Sensitivity] | None = None
    elements: dict[str, Sensitivity | dict[str, Sensitivity]] | None = None


class CustomConfig(RootModel):
    """Model for the default configuration."""

    root: dict[str, CustomTypeConfig]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


    @model_validator(mode="after")
    def check_elements(self):
        """Check that all types, attributes, and elements in the configuration are known found in the structure."""
        all_types = set(structure)
        all_in_config = set(self)
        unknown_types = all_in_config - all_types
        if unknown_types:
            raise ValueError(f"Unknown types in default configuration: {', '.join(unknown_types)}")

        for type_name, type_config in self.items():
            # Check attributes
            all_attributes = set(structure[type_name]["attributes"])
            all_attributes_in_config = set(type_config.attributes)
            unknown_attributes = all_attributes_in_config - all_attributes
            if unknown_attributes:
                raise ValueError(f"Unknown attributes in type '{type_name}': {', '.join(unknown_attributes)}")

            all_elements = set(structure[type_name]["elements"])
            all_elements_in_config = set(type_config.elements)
            unknown_elements = all_elements_in_config - all_elements
            if unknown_elements:
                raise ValueError(f"Unknown elements in type '{type_name}': {', '.join(unknown_elements)}")

            # Check elements
            for elem, elem_config in type_config.elements.items():
                if isinstance(elem_config, dict):
                    all_subelements = set(structure[type_name]["elements"][elem])
                    all_subelements_in_config = set(elem_config)
                    unknown_subelements = all_subelements_in_config - all_subelements
                    if unknown_subelements:
                        raise ValueError(f"Unknown sub-elements in element '{elem}' of type '{type_name}': {', '.join(unknown_subelements)}")


class DefaultTypeConfig(BaseModel):
    """Model for the default configuration of a type.

    This is used to define the default configuration for types in the `CustomConfig`.
    """

    text_content: Sensitivity
    attributes: dict[str, Sensitivity]
    elements: dict[str, Sensitivity | dict[str, Sensitivity]]

class DefaultConfig(CustomConfig):

    @model_validator(mode="after")
    def check_elements(self):
        """Check that all types, attributes, and elements in the configuration are known found in the structure."""
        all_types = set(structure)
        all_in_config = set(self)
        missing_types = all_types - all_in_config
        if missing_types:
            raise ValueError(f"Missing types in default configuration: {', '.join(missing_types)}")

        unknown_types = all_in_config - all_types
        if unknown_types:
            raise ValueError(f"Unknown types in default configuration: {', '.join(unknown_types)}")

        for type_name, type_config in self.items():
            # Check attributes
            all_attributes = set(structure[type_name]["attributes"])
            all_attributes_in_config = set(type_config.attributes)
            missing_attributes = all_attributes - all_attributes_in_config
            if missing_attributes:
                raise ValueError(f"Missing attributes in type '{type_name}': {', '.join(missing_attributes)}")
            unknown_attributes = all_attributes_in_config - all_attributes
            if unknown_attributes:
                raise ValueError(f"Unknown attributes in type '{type_name}': {', '.join(unknown_attributes)}")

            all_elements = set(structure[type_name]["elements"])
            all_elements_in_config = set(type_config.elements)
            missing_elements = all_elements - all_elements_in_config
            if missing_elements:
                raise ValueError(f"Missing elements in type '{type_name}': {', '.join(missing_elements)}")
            unknown_elements = all_elements_in_config - all_elements
            if unknown_elements:
                raise ValueError(f"Unknown elements in type '{type_name}': {', '.join(unknown_elements)}")

            # Check elements
            for elem, elem_config in type_config.elements.items():
                if isinstance(elem_config, dict):
                    all_subelements = set(structure[type_name]["elements"][elem])
                    all_subelements_in_config = set(elem_config)
                    missing_subelements = all_subelements - all_subelements_in_config
                    if missing_subelements:
                        raise ValueError(f"Missing sub-elements in element '{elem}' of type '{type_name}': {', '.join(missing_subelements)}")
                    unknown_subelements = all_subelements_in_config - all_subelements
                    if unknown_subelements:
                        raise ValueError(f"Unknown sub-elements in element '{elem}' of type '{type_name}': {', '.join(unknown_subelements)}")
