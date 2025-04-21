from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.BL import BL
from CDA.logical_models.CE import CE
from CDA.logical_models.ED import ED
from CDA.logical_models.II import II
from CDA.logical_models.PN import PN
from CDA.logical_models.TS import TS


class SubjectPerson(BaseModel):
    """Logical Model: SubjectPerson (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SubjectPerson.html
    """

    classCode: Literal["PSN"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassLivingSubject",
            "binding_strength": "required",
            "fixed_value": "PSN",
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
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    name: list[PN] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    desc: ED | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    administrativeGenderCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "AdministrativeGender",
            "binding_strength": "extensible",
        }
    )
    birthTime: TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    deceasedInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    deceasedTime: TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
