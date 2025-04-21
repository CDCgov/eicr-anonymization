from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CE import CE
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Performer1 import Performer1
from CDA.value_sets.ActMood import ActMood


class ServiceEvent(BaseModel):
    """Logical Model: ServiceEvent (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ServiceEvent.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClass",
            "binding_strength": "required",
        }
    )
    moodCode: Literal[ActMood.EVN] | None = Field(
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
        }
    )
    effectiveTime: IVL_TS | None = Field(json_schema_extra={"xml_type": "element"})
    performer: list[Performer1] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
