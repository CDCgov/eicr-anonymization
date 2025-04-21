from typing import Literal

from pydantic import Field, model_validator

from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.NonXMLBody import NonXMLBody
from CDA.logical_models.StructuredBody import StructuredBody


class Component(InfrastructureRoot):
    """Logical Model: Component (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Component.html
    """

    typeCode: Literal["COMP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActRelationshipHasComponent",
            "binding_strength": "required",
        }
    )
    contextConductionInd: Literal["true"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "true",
        }
    )
    nonXMLBody: NonXMLBody | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    structuredBody: StructuredBody | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )

    @model_validator(mode="after")
    def body_choice(self):
        """Choice of the body required."""
        if (self.nonXMLBody and self.structuredBody) or (
            not self.nonXMLBody and not self.structuredBody
        ):
            raise ValueError("Choice of the body required.")
        return self
