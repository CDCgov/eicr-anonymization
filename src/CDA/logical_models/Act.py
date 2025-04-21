from pydantic import BaseModel, Field

from CDA.data_types.string_validators import bl, cs
from CDA.logical_models.Author import Author
from CDA.logical_models.CD import CD
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.ED import ED
from CDA.logical_models.EntryRelationship import EntryRelationship
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Participant2 import Participant2
from CDA.logical_models.Performer2 import Performer2
from CDA.logical_models.Precondition import Precondition
from CDA.logical_models.Reference import Reference
from CDA.logical_models.Specimen import Specimen
from CDA.logical_models.Subject import Subject
from CDA.value_sets.NullFlavor import NullFlavor


class Act(BaseModel):
    """Logical Model: Act (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Act.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    moodCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        },
    )
    code: CD = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode",
            "binding_strength": "extensible",
        }
    )
    negationInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    text: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
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
    priorityCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActPriority",
        }
    )
    languageCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "HumanLanguage",
            "binding_strength": "required",
        }
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
