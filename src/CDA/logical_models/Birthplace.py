"""Logical Model: Birthplace (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Birthplace.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.Place import Place


class Birthplace(BaseModel):
    """Logical Model: Birthplace (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Birthplace.html
    """

    classCode: Literal["BIRTHPL"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassPassive",
            "binding_strength": "required",
            "fixed_value": "BIRTHPL",
        }
    )
    templateId: list[str] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    place: Place = Field(
        json_schema_extra={"xml_type": "element"},
    )
