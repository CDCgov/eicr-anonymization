"""Logical Model: OrganizationPartOf (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-OrganizationPartOf.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Organization import Organization


class OrganizationPartOf(BaseModel):
    """Logical Model: OrganizationPartOf (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-OrganizationPartOf.html
    """

    classCode: Literal["PART"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassPartitive",
            "binding_strength": "required",
            "fixed_value": "PART",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    identifiedBy: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System RoleCode",
            "binding_strength": "required",
        }
    )
    statusCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    effectiveTime: IVL_TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    wholeOrganization: Organization | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
