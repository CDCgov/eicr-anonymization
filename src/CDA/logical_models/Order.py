from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CE import CE
from CDA.logical_models.II import II


class Order(BaseModel):
    """Logical Model: Order (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Order.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClass",
            "binding_strength": "required",
        }
    )
    moodCode: Literal["RQO"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMoodIntent",
            "binding_strength": "required",
            "fixed_value": "RQO",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] = Field(json_schema_extra={"xml_type": "element"}, min_length=1)
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode ",
        }
    )
    priorityCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActPriority",
        }
    )
