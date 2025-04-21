"""Logical Model: AlternateIdentification (CDA Class) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AlternateIdentification.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CD import CD
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS


class AlternateIdentification(BaseModel):
    """Logical Model: AlternateIdentification (CDA Class) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AlternateIdentification.html
    """

    classCode: Literal["IDENT"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": "IDENT",
        }
    )
    id: II = Field(json_schema_extra={"xml_type": "element"})
    code: CD | None = Field(json_schema_extra={"xml_type": "element"})
    statusCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActStatus",
            "binding_strength": "required",
        }
    )
    effectiveTime: IVL_TS = Field(json_schema_extra={"xml_type": "element"})
