"""Logical Model: MaintainedEntity (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-MaintainedEntity.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Person import Person


class MaintainedEntity(BaseModel):
    """Logical Model: MaintainedEntity (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-MaintainedEntity.html
    """

    classCode: Literal["MNT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassPassive",
            "binding_strength": "required",
            "fixed_value": "MNT",
        }
    )
    templateID: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    effectiveTime: IVL_TS | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    maintainingPerson: Person = Field(
        json_schema_extra={"xml_type": "element"},
    )
