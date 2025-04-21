from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.value_sets.NullFlavor import NullFlavor


class Participant1(BaseModel):
    """Logical Model: Participant1 (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Participant1.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
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
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    functionCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    time: IVL_TS | None = Field(json_schema_extra={"xml_type": "element"})
    assignedEntity: AssignedEntity = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
