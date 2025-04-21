"""Logical Model: IdentifiedBy (CDA Class) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IdentifiedBy.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AlternateIdentification import AlternateIdentification


class IdentifiedBy(BaseModel):
    """Logical Model: IdentifiedBy (CDA Class) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IdentifiedBy.html
    """

    typeCode: Literal["REL"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleLinkType",
            "binding_strength": "required",
            "fixed_value": "REL",
        }
    )
    alternateIdentification: AlternateIdentification = Field(
        json_schema_extra={"xml_type": "element"}
    )
