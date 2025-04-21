from typing import Literal

from pydantic import Field

from CDA.logical_models.CE import CE
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.RelatedSubject import RelatedSubject


class Subject(InfrastructureRoot):
    """Logical Model: Subject (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Subject.html
    """

    typeCode: Literal["SBJP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationTargetSubject",
            "binding_strength": "required",
            "fixed_value": "SBJP",
        }
    )
    contextControlCode: Literal["OP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ContextControl",
            "binding_strength": "required",
        }
    )
    awerenessCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "TargetAwareness",
            "binding_strength": "extensible",
        }
    )
    relatedSubject: RelatedSubject = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
