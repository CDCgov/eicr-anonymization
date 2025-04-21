from pydantic import Field, model_validator

from CDA.data_types.string_validators import cs
from CDA.logical_models.BL import BL
from CDA.logical_models.ExternalAct import ExternalAct
from CDA.logical_models.ExternalDocument import ExternalDocument
from CDA.logical_models.ExternalObservation import ExternalObservation
from CDA.logical_models.ExternalProcedure import ExternalProcedure
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot


class Reference(InfrastructureRoot):
    """Logical Model: Reference (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Reference.html
    """

    typeCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "x_ActRelationshipExternalReference",
            "binding_strength": "required",
        }
    )
    seperatableInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    externalAct: ExternalAct | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    externalObservation: ExternalObservation | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    externalProcedure: ExternalProcedure | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    externalDocument: ExternalDocument | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )

    @model_validator(mode="after")
    def reference_external(self):
        """Must contain one (and only one) external reference."""
        count = 0
        if self.externalAct:
            count += 1
        if self.externalObservation:
            count += 1
        if self.externalProcedure:
            count += 1
        if self.externalDocument:
            count += 1
        if count != 1:
            raise ValueError("Reference must contain one (and only one) external reference.")

        return self
