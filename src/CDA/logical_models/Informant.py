"""Logical Model: Informant (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Informant.html
"""

from typing import Literal

from pydantic import Field, model_validator

from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.RelatedEntity import RelatedEntity


class Informant(InfrastructureRoot):
    """Logical Model: Informant (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Informant.html
    """

    typeCode: Literal["INF"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "INF",
        }
    )
    contextControlCode: Literal["OP"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ContextControl",
            "binding_strength": "required",
            "fixed_value": "OP",
        }
    )
    assignedEntity: AssignedEntity | None = Field(json_schema_extra={"xml_type": "element"})
    relatedEntity: RelatedEntity | None = Field(json_schema_extra={"xml_type": "element"})

    @model_validator(mode="after")
    def informant_entity(self) -> "Informant":
        """Ensure that the relatedPerson is not None if classCode is 'ENT'."""
        if self.assignedEntity is not None and self.relatedEntity is not None:
            raise ValueError(
                "AssignedEntity and RelatedEntity are mutually exclusive (one must be present)."
            )
        return self
