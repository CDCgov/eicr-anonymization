from typing import Literal

from pydantic import Field

from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.ED import ED
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.value_sets.ActClass import ActClass
from CDA.value_sets.ActMood import ActMood


class NonXMLBody(InfrastructureRoot):
    """Logical Model: NonXMLBody (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-NonXMLBody.html
    """

    classCode: Literal[ActClass.DOCBODY] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": ActClass.DOCBODY,
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
    text: ED = Field(
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
