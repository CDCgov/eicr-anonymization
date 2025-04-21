"""Logical Model: ST: CharacterString (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ST.html
"""

from typing import Literal

from pydantic import Field

from CDA.data_types.string_validators import cs, st
from CDA.logical_models.ANY import ANY


class ST(ANY):
    """Logical Model: ST: CharacterString (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ST.html
    """

    representation: Literal["TXT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "TXT",
        }
    )
    mediaType: Literal["text/plain"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "text/plain",
        }
    )
    language: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    xmlText: st | None = Field(
        description="Allows for mixed text content",
        json_schema_extra={
            "xml_type": "text",
        },
    )
