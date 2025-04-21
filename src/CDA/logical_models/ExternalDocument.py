from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CD import CD
from CDA.logical_models.ED import ED
from CDA.logical_models.II import II
from CDA.value_sets.ActMood import ActMood


class ExternalDocument(BaseModel):
    """Logical Model: ExternalDocument (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Reference.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClass",
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
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode",
            "binding_strength": "extensible",
        }
    )
    text: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
