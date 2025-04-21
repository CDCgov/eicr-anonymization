from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CE import CE
from CDA.logical_models.ED import ED
from CDA.logical_models.II import II
from CDA.logical_models.PN import PN
from CDA.logical_models.PQ import PQ
from CDA.logical_models.TS import TS


class PlayingEntity(BaseModel):
    """Logical Model: PlayingEntity (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PlayingEntity.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassRoot",
            "binding_strength": "required",
        }
    )
    determinerCode: Literal["INSTANCE"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityDeterminer",
            "binding_strength": "required",
            "fixed_value": "INSTANCE",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "EntityCode",
            "binding_strength": "extensible",
        }
    )
    quantity: list[PQ] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "EntityQuantity",
            "binding_strength": "extensible",
        }
    )
    name: list[PN] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    birthTime: TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    desc: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
