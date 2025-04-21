"""Logical Model: RecordTarget (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RecordTarget.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.PatientRole import PatientRole
from CDA.value_sets.NullFlavor import NullFlavor


class RecordTarget(BaseModel):
    """Logical Model: RecordTarget (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RecordTarget.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["RCT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "PartipationType",
            "binding_strength": "required",
            "fixed_value": "RCT",
        }
    )
    contextControlCode: Literal["OP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ContextControl",
            "binding_strength": "required",
            "fixed_value": "OP",
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
    patientRole: PatientRole = Field(
        json_schema_extra={"xml_type": "element"},
    )
