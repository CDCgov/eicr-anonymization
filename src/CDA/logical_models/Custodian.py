"""Logical Model: Custodian (CDA Class).

http://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Custodian.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AssignedCustodian import AssignedCustodian
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.value_sets.NullFlavor import NullFlavor


class Custodian(BaseModel):
    """Logical Model: Custodian (CDA Class).

    http://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Custodian.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["ENT"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    assignedCustodian: AssignedCustodian = Field(json_schema_extra={"xml_type": "element"})
