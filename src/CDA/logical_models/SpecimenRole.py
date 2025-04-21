from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.PlayingEntity import PlayingEntity


class SpecimenRole(BaseModel):
    """Logical Model: SpecimenRole (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SpecimenRole.html
    """

    classCode: Literal["SPEC"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": "SPEC",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    identifiedBy: list[IdentifiedBy] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    specimenPlayingEntity: PlayingEntity | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
