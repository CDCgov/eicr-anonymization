from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.value_sets.ActClass import ActClass
from CDA.value_sets.ActMood import ActMood


class _statusCode(CS):
    """A specialized CS for statusCode to capture requirements from Consent."""

    code: Literal["completed"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "completed",
        }
    )


class Consent(BaseModel):
    """Logical Model: Consent (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Consent.html
    """

    classCode: Literal[ActClass.CONS] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": ActClass.CONS,
        }
    )
    moodCode: Literal[ActMood.EVN] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMood",
            "binding_strength": "required",
            "fixed_value": ActMood.EVN,
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode",
            "binding_strength": "extensible",
        }
    )
    statusCode: _statusCode = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActStatus",
            "binding_strength": "required",
        }
    )
