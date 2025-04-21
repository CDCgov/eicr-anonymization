from typing import Any, Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import bl, id
from CDA.logical_models.Author import Author
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.Entry import Entry
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.ST import ST
from CDA.logical_models.Subject import Subject
from CDA.value_sets.ActClass import ActClass
from CDA.value_sets.ActMood import ActMood
from CDA.value_sets.NullFlavor import NullFlavor


class _component(InfrastructureRoot):
    """Specialized model of InfrastructureRoot for section."""

    typeCode: Literal["COMP"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding_strength": "required",
            "fixed_value": "COMP",
        }
    )
    contextConductionInd: Literal["true"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding_strength": "required",
            "fixed_value": "true",
        }
    )
    section: "Section" = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )


class Section(BaseModel):
    """Logical Model: Section (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Section.html
    """

    ID: id | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    classCode: Literal[ActClass.DOCSECT] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": ActClass.DOCSECT,
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
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: II | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "DocumentSectionType",
            "binding_strength": "extensible",
        }
    )
    title: ST | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    text: Any | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    confidentialityCode: list[CE] | None = Field(
        json_schema_extra={
            "xml_type": "element",
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
    author: list[Author] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    informant: list[Informant] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    entry: list[Entry] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    component: list[_component] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
