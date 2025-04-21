from typing import Literal

from pydantic import Field

from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.Section import Section
from CDA.value_sets.ActMood import ActMood


class _component(InfrastructureRoot):
    """Specialized InfrastructureRoot for StructuredBody component."""

    typeCode: Literal["COMP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "COMP",
        }
    )
    contextConductionInd: Literal["true"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "Fixed_value": "true",
        }
    )
    section: Section = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )


class StructuredBody(InfrastructureRoot):
    """Logical Model: StructuredBody (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-StructuredBody.html
    """

    classCode: Literal["DOCBODY"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClassRecordOrganizer",
            "binding_strength": "required",
            "fixed_value": "DOCBODY",
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
    component: list[_component] = Field(
        json_schema_extra={
            "xml_type": "element",
        },
        min_length=1,
    )
