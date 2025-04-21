from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.Author import Author
from CDA.logical_models.CD import CD
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Informant import Informant
from CDA.logical_models.OrganizerComponent import OrganizerComponent
from CDA.logical_models.Participant2 import Participant2
from CDA.logical_models.Performer2 import Performer2
from CDA.logical_models.Precondition import Precondition
from CDA.logical_models.Reference import Reference
from CDA.logical_models.Specimen import Specimen
from CDA.logical_models.Subject import Subject
from CDA.value_sets.ActMood import ActMood


class Organizer(BaseModel):
    """Logical Model: Organizer (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Organizer.html
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
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode",
            "binding_strength": "extensible",
        }
    )
    statusCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActStatus",
            "binding_strength": "required",
        }
    )
    effectiveTime: IVL_TS = Field(json_schema_extra={"xml_type": "element"})
    subject: Subject | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    specimen: list[Specimen] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    performer: list[Performer2] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    author: list[Author] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    informant: list[Informant] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    participant: list[Participant2] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    reference: list[Reference] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    precondition: list[Precondition] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    component: list[OrganizerComponent] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
