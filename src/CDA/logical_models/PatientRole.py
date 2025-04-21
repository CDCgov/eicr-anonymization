"""Logical Model: PatientRole (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PatientRole.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.TEL import TEL


class PatientRole(BaseModel):
    """Logical Model: PatientRole (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PatientRole.html
    """

    classCode: Literal["PAT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": "PAT",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    identifiedBy: list[IdentifiedBy] = Field(json_schema_extra={"xml_type": "element"})
    addr: list[AD] | None = Field(json_schema_extra={"xml_type": "element"})
    telecom: list[TEL] | None = Field(json_schema_extra={"xml_type": "element"})
    patient: Patient | None = Field(json_schema_extra={"xml_type": "element"})
    providerOrganization: Organization | None = Field(json_schema_extra={"xml_type": "element"})
