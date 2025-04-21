"""Logical Model: Person (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Person.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.II import II
from CDA.logical_models.PN import PN


class Person(BaseModel):
    """Logical Model: Person (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Person.html
    """

    classCode: Literal["PSN"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassLivingSubject",
            "binding_strength": "required",
            "fixed_value": "PSN",
        }
    )
    determinerCode: Literal["INSTANCE"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityDeterminer",
            "binding_strength": "required",
            "fixed_value": "INSTANCE",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    name: list[PN] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    asPatientRelationship: list[CE] | None = Field(json_schema_extra={"xml_type": "element"})
