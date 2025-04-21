"""Logical Model: AssignedAuthor (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedAuthor.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.AuthoringDevice import AuthoringDevice
from CDA.logical_models.CE import CE
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.Organization import Organization
from CDA.logical_models.Person import Person
from CDA.logical_models.TEL import TEL


class AssignedAuthor(BaseModel):
    """Logical Model: AssignedAuthor (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedAuthor.html
    """

    classCode: Literal["ASSIGNED"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassAssignedEntity",
            "binding_strength": "required",
            "fixed_value": "ASSIGNED",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: list[II] = Field(json_schema_extra={"xml_type": "element"}, min_length=1)
    identifiedBy: list[IdentifiedBy] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System RoleCode",
            "binding_strength": "extensible",
        }
    )
    addr: list[AD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    assignedPerson: Person | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    assignedAuthoringDevice: AuthoringDevice | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    representedOrganization: Organization | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
