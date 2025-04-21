"""Logical Model: Guardian (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Guardian.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.CE import CE
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.Organization import Organization
from CDA.logical_models.Person import Person
from CDA.logical_models.TEL import TEL


class Guardian(BaseModel):
    """Logical Model: Guardian (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Guardian.html
    """

    classCode: Literal["GAURD"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassAgent",
            "binding_strength": "required",
            "fixed_value": "GAURD",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    identifiedBy: list[IdentifiedBy] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": " v3 Code System RoleCode",
            "binding_strength": "required",
        }
    )
    addr: list[AD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    guardianPerson: Person | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    guardianOrganization: Organization | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
