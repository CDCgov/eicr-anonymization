from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.value_sets.NullFlavor import NullFlavor


class Performer2(BaseModel):
    """Logical Model: Performer2 (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Performer2.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["PRF"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationPhysicalPerformer",
            "binding_strength": "required",
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
    moodCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    assignedEntity: AssignedEntity = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
