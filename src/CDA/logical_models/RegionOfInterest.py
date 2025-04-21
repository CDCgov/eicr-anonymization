from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import id
from CDA.logical_models.Author import Author
from CDA.logical_models.CS import CS
from CDA.logical_models.EntryRelationship import EntryRelationship
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.INT import INT
from CDA.logical_models.Participant2 import Participant2
from CDA.logical_models.Performer2 import Performer2
from CDA.logical_models.Precondition import Precondition
from CDA.logical_models.Reference import Reference
from CDA.logical_models.Specimen import Specimen
from CDA.logical_models.Subject import Subject
from CDA.value_sets.ActMood import ActMood


class RegionOfInterest(BaseModel):
    """Logical Model: RegionOfInterest (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RegionOfInterest.html
    """

    ID: id | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    classCode: Literal["ROIOVL"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClassROI",
            "binding_strength": "required",
            "fixed_value": "ROIOVL",
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
    id: list[II] = Field(
        min_length=1,
        json_schema_extra={
            "xml_type": "element",
        },
    )
    code: CS = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    value: list[INT] = Field(
        min_length=1,
        json_schema_extra={
            "xml_type": "element",
        },
    )
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
    entryRelationship: list[EntryRelationship] | None = Field(
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
