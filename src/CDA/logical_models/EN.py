"""Logical Model: EN: EntityName (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EN.html
"""

from pydantic import Field

from CDA.data_types.string_validators import cs, st
from CDA.logical_models.ANY import ANY
from CDA.logical_models.ENXP import ENXP
from CDA.logical_models.IVL_TS import IVL_TS


class EN(ANY):
    """Logical Model: EN: EntityName (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EN.html
    """

    use: list[cs] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityNameUse",
            "binding_strength": "required",
        },
    )
    delimiter: list[ENXP] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    family: list[ENXP] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    given: list[ENXP] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    prefix: list[ENXP] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    suffix: list[ENXP] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    xmlText: st | None = Field(
        description="Allows for mixed text content",
        json_schema_extra={"xml_type": "text"},
    )
    validTime: IVL_TS | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
