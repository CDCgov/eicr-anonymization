"""Extracts the structure for a CDA from the FHIR definitions into a YAML.

This expects the FHIR definitions to be in JSON format in the directory `tools/fhir_definitions` and
saves the output YAML into `src/eicr_anonymization`.
"""

import json
import re
from pathlib import Path

import yaml


def read_all_jsons(directory_path):
    """
    Read all JSON files in a directory and return their contents.

    Args:
        directory_path (str): Path to the directory containing JSON files

    Returns:
        dict: Dictionary with filename as key and JSON content as value
    """
    json_data: list[dict] = []

    # Convert to Path object for easier handling
    dir_path = Path(directory_path)

    # Check if directory exists
    if not dir_path.exists():
        print(f"Directory {directory_path} does not exist")
        return json_data

    # Find all JSON files
    json_files = dir_path.glob("*.json")

    for json_file in json_files:
        try:
            with open(json_file, encoding="utf-8") as file:
                json_data.append(json.load(file))

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {json_file.name}: {e}")
        except Exception as e:
            print(f"Error reading {json_file.name}: {e}")

    return json_data


def get_default_value(element):
    if "extension" in element:
        for ext in element["extension"]:
            if (
                ext.get("url")
                == "http://hl7.org/fhir/StructureDefinition/elementdefinition-defaulttype"
            ):
                return ext.get("valueCanonical", "").split("/")[-1]
    return None


def sanitize_name(name: str):
    """
    Sanitize names by replacing spaces with underscores and converting to lowercase.

    Args:
        name (str): The name to sanitize

    Returns:
        str: Sanitized name
    """
    if name is None:
        return None
    name = re.split(r"[/}\.]", name)[-1].replace("-", "_")

    if name.startswith("sdtc"):
        name = name[4:]
        name = name[0].lower() + name[1:]

    return name


if __name__ == "__main__":
    # Replace with your directory path
    directory = "tools/fhir_definition"

    all_json_data = read_all_jsons(directory)
    data_types = {}

    for definition in all_json_data:
        if (
            definition.get("resourceType") != "StructureDefinition"
            or definition.get("kind") == "primitive-type"
        ):
            continue
        name = sanitize_name(definition["id"])
        print(name)
        attributes = {}
        children = {}

        choice_group_element = None
        has_subelements = []
        for element in definition["snapshot"]["element"]:
            is_choice_group = False
            path = element["path"].split(".")
            if choice_group_element and choice_group_element in path:
                path.remove(choice_group_element)
            if len(path) == 1:
                continue
            elif len(path) == 2:
                if element.get("extension") and any(
                    ext.get("url")
                    == "http://hl7.org/fhir/tools/StructureDefinition/xml-choice-group"
                    for ext in element["extension"]
                ):
                    # Skip the element defining a choice group but we still need the elements
                    choice_group_element = element["id"].split(".")[-1]
                    is_choice_group = True
                if is_choice_group:
                    continue

                element_name = sanitize_name(element["id"])
                if "xmlAttr" in element.get("representation", []):
                    attributes[element_name] = next(
                        sanitize_name(element_type["code"]) for element_type in element["type"]
                    )
                else:
                    children[element_name] = {
                        "types": [
                            sanitize_name(element_type["code"]) for element_type in element["type"]
                        ],
                        "default_type": sanitize_name(get_default_value(element)),
                    }
                    if (
                        "type" in element
                        and element["type"][0]["code"]
                        == "http://hl7.org/cda/stds/core/StructureDefinition/InfrastructureRoot"
                    ):
                        has_subelements.append(element_name)
            elif len(path) == 3 and "type" in element and path[1] in has_subelements:
                if "xmlAttr" in element.get("representation", []):
                    children[sanitize_name(path[1])].setdefault("attributes", {})[
                        sanitize_name(element["id"])
                    ] = next(
                        sanitize_name(element_type["code"]) for element_type in element["type"]
                    )
                else:
                    children[sanitize_name(path[1])].setdefault("elements", {})[
                        sanitize_name(element["id"])
                    ] = {
                        "types": [
                            sanitize_name(element_type["code"]) for element_type in element["type"]
                        ],
                        "default_type": sanitize_name(get_default_value(element)),
                    }

        data_types[name] = {"attributes": attributes, "elements": children}

    with open("schema_structure_from_fhir.yaml", "w") as file:
        yaml.dump(data_types, file, sort_keys=False)
