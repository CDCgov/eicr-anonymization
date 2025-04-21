"""Logical Model: AssignedCustodian (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedCustodian.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CustodianOrganization import CustodianOrganization
from CDA.logical_models.II import II


class AssignedCustodian(BaseModel):
    """Logical Model: AssignedCustodian (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AssignedCustodian.html
    """

    classCode: Literal["ASSIGNED"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleAssignedEntity",
            "binding_strength": "required",
            "fixed_value": "ASSIGNED",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    representedCustodianOrganization: CustodianOrganization = Field(
        json_schema_extra={"xml_type": "element"}
    )
