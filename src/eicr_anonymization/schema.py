from collections import OrderedDict

import yaml
from lxml import etree

restrictions_map = {}


def parse_xsd_simple(schema_path: str):
    tree = etree.parse(schema_path)
    root = tree.getroot()

    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    data_types = {}

    # Find all complexType definitions
    for complex_type in root.xpath("//xs:complexType[@name]", namespaces=ns):
        type_name = complex_type.get("name").removeprefix("hl7:").removeprefix("POCD_MT000040.")
        removes = []

        extension = complex_type.find(".//xs:extension", namespaces=ns)
        extends = None
        if extension is not None:
            extends = extension.get("base", "").removeprefix("hl7:").removeprefix("POCD_MT000040.")

        restriction = complex_type.find(".//xs:restriction", namespaces=ns)
        if restriction is not None:
            extends = (
                restriction.get("base", "").removeprefix("hl7:").removeprefix("POCD_MT000040.")
            )
            restrictions_map[type_name] = extends

            for restriction_element in restriction.xpath(
                ".//xs:element[@name and @maxOccurs='0'] | .//xs:attribute[@name and @use='prohibited']",
                namespaces=ns,
            ):
                removes.append(restriction_element.get("name"))

        elements = {}
        attributes = {}

        # Find child elements
        for element in complex_type.xpath(".//xs:element[@name]", namespaces=ns):
            elem_name = element.get("name")
            if element.get("maxOccurs") == "0":
                removes.append(elem_name)
            else:
                elem_type = (
                    element.get("type", "").removeprefix("hl7:").removeprefix("POCD_MT000040.")
                )
                elements[elem_name] = elem_type

        # Find attributes
        for attr in complex_type.xpath(
            ".//xs:attribute[@name and not(@use='prohibited')]", namespaces=ns
        ):
            attr_name = attr.get("name")
            if attr.get("use") == "prohibited":
                removes.append(attr_name)
            else:
                attr_type = (
                    attr.get("type", "")
                    .split("_")[-1]
                    .removeprefix("hl7:")
                    .removeprefix("POCD_MT000040.")
                )
                attributes[attr_name] = attr_type

        for element in complex_type.xpath(".//xs:element[@ref]", namespaces=ns):
            if element.get("ref").startswith("sdtc:"):
                elem_name = element.get("ref").removeprefix("sdtc:")
                if element.get("maxOccurs") == "0":
                    removes.append(elem_name)
                else:
                    elem_type = sdtc_type_mapping[elem_name]
                    elements[elem_name] = elem_type

        for attr in complex_type.xpath(".//xs:attribute[@ref]", namespaces=ns):
            if attr.get("ref").startswith("sdtc:"):
                attr_name = attr.get("ref").removeprefix("sdtc:")
                if attr.get("use") == "prohibited":
                    removes.append(attr_name)
                else:
                    attr_type = sdtc_type_mapping[attr_name]
                    attributes[attr_name] = attr_type

        data_types[type_name] = {
            "extends": extends,
            "extended_by": [],
            "attributes": attributes,
            "elements": elements,
            "removes": removes,
        }

    return data_types


# Usage
schema_paths = [
    "src/eicr_anonymization/schema/SDTC/infrastructure/cda/POCD_MT000040_SDTC.xsd",
    "src/eicr_anonymization/schema/SDTC/infrastructure/cda/SDTC.xsd",
    "src/eicr_anonymization/schema/SDTC/processable/coreschemas/datatypes-base_SDTC.xsd",
    "src/eicr_anonymization/schema/SDTC/processable/coreschemas/datatypes.xsd",
]


def collect_elements(data_type_name: str) -> dict[str, str]:
    own_elements = {
        k: v
        for k, v in data_types[data_type_name]["elements"].items()
        if k not in data_types[data_type_name]["removes"]
    }
    if data_types[data_type_name]["extends"]:
        ancestors_elements = collect_elements(data_types[data_type_name]["extends"])

        filter_ancestors_elements = {
            k: v
            for k, v in ancestors_elements.items()
            if k not in data_types[data_type_name]["removes"]
        }

        return own_elements | filter_ancestors_elements
    else:
        return own_elements


def collect_attributes(data_type_name: str) -> dict[str, str]:
    own_elements = {
        k: v
        for k, v in data_types[data_type_name]["attributes"].items()
        if k not in data_types[data_type_name]["removes"]
    }
    if data_types[data_type_name]["extends"]:
        ancestors_elements = collect_attributes(data_types[data_type_name]["extends"])

        filter_ancestors_elements = {
            k: v
            for k, v in ancestors_elements.items()
            if k not in data_types[data_type_name]["removes"]
        }

        return own_elements | filter_ancestors_elements
    else:
        return own_elements


data_types = {}


def get_sdtc_type_mapping():
    tree = etree.parse("src/eicr_anonymization/schema/SDTC/infrastructure/cda/SDTC.xsd")
    root = tree.getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}

    sdtc_type_map = {}
    for element in root.xpath(
        "//xs:element[@name and @type] | //xs:attribute[@name and @type]", namespaces=ns
    ):
        element_name = element.get("name")
        element_type = element.get("type", "")
        sdtc_type_map[element_name] = element_type.removeprefix("hl7:")

    return sdtc_type_map


sdtc_type_mapping = get_sdtc_type_mapping()
for schema_path in schema_paths:
    data_types = data_types | parse_xsd_simple(schema_path)

for data_type in data_types.values():
    for child_name, child_type in data_type["elements"].items():
        if child_type in restrictions_map and "." in child_type:
            data_type["elements"][child_name] = restrictions_map[child_type]

for data_type_name, data_type in data_types.items():
    if data_type["extends"]:
        data_types[data_type["extends"]]["extended_by"].append(data_type_name)

    data_type["elements"] = collect_elements(data_type_name)
    data_type["attributes"] = collect_attributes(data_type_name)


for data_type in restrictions_map:
    if "." in data_type:
        del data_types[data_type]

# Clean output
with open("schema_structure.yaml", "w") as file:
    yaml.dump(data_types, file, sort_keys=False)

# Print summary
print(f"Extracted {len(data_types)} types")
for type_name, info in list(data_types.items())[:5]:  # Show first 5
    print(f"\n{type_name}:")
    if info.get("elements"):
        print(f"  Elements: {list(info['elements'].keys())}")
    if info.get("attributes"):
        print(f"  Attributes: {list(info['attributes'].keys())}")
