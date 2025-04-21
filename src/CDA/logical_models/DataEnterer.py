"""Logical Model: DataEnterer (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-DataEnterer.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.II import II
from CDA.logical_models.TS import TS
from CDA.value_sets.NullFlavor import NullFlavor


class DataEnterer(BaseModel):
    """Logical Model: DataEnterer (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-DataEnterer.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["ENT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "ENT",
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
    realmCode: list[cs] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    time: TS = Field(json_schema_extra={"xml_type": "element"})
    assignedEntity: AssignedEntity = Field(json_schema_extra={"xml_type": "element"})
