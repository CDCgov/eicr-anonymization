"""Logical Model: Place (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Place.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.EN import EN
from CDA.logical_models.II import II


class Place(BaseModel):
    """Logical Model: Place (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Place.html
    """

    classCode: Literal["PLC"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassPlace",
            "binding_strength": "required",
            "fixed_value": "PLC",
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
    name: EN | None = Field(json_schema_extra={"xml_type": "element"})
    addr: AD | None = Field(json_schema_extra={"xml_type": "element"})
