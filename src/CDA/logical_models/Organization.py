"""Logical Model: Organization (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Organization.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.ON import ON
from CDA.logical_models.OrganizationPartOf import OrganizationPartOf
from CDA.logical_models.TEL import TEL
from CDA.value_sets.NullFlavor import NullFlavor


class Organization(BaseModel):
    """Logical Model: Organization (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Organization.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    classCode: Literal["ORG"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassOrganization",
            "binding_strength": "required",
            "fixed_value": "ORG",
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
    realmCode: list[CS] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    typeId: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    name: list[ON] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    addr: list[AD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    standardIndustryClassCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "OrganizationIndustryClassNAICS",
            "binding_strength": "extensible",
        }
    )
    asOrganizationPartOf: OrganizationPartOf | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
