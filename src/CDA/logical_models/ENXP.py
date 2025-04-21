"""Logical Model: ENXP: Entity Name Part (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ENXP.html
"""

from pydantic import Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.ST import ST


class ENXP(ST):
    """Logical Model: ENXP: Entity Name Part (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ENXP.html
    """

    partType: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityNamePartType",
            "binding_strength": "required",
        },
    )
    qualifier: list[cs] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityNamePartQualifier",
            "binding_strength": "required",
        },
    )
