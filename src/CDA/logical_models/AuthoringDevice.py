"""Logical Model: AuthoringDevice (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AuthoringDevice.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.II import II
from CDA.logical_models.MaintainedEntity import MaintainedEntity
from CDA.logical_models.SC import SC


class AuthoringDevice(BaseModel):
    """Logical Model: AuthoringDevice (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AuthoringDevice.html
    """

    classCode: Literal["DEV"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassDevice",
            "binding_strength": "required",
            "fixed_value": "DEV",
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
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "EntityCoode",
            "binding_strength": "extensible",
        }
    )
    manufacturerModelName: SC | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "Manufacturer Model Name Example",
            "binding_strength": "example",
        },
    )
    softwareName: SC | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "Software Name Example",
            "binding_strength": "example",
        },
    )
    asMaintainedEntity: list[MaintainedEntity] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
