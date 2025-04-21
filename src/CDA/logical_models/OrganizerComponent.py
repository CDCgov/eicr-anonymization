from typing import Literal

from pydantic import Field, model_validator

from CDA.data_types.string_validators import cs
from CDA.logical_models.Act import Act
from CDA.logical_models.BL import BL
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.INT import INT
from CDA.logical_models.Observation import Observation
from CDA.logical_models.ObservationMedia import ObservationMedia
from CDA.logical_models.Organizer import Organizer
from CDA.logical_models.Procedure import Procedure
from CDA.logical_models.RegionOfInterest import RegionOfInterest
from CDA.logical_models.SubstanceAdministration import SubstanceAdministration
from CDA.logical_models.Supply import Supply


class OrganizerComponent(InfrastructureRoot):
    """OrganizerComponent (CDA Class) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-OrganizerComponent.html
    """

    typeCode: cs | None = Field(
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
    sequenceNumber: INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    priorityNumber: INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    seperatableInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    act: Act | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    observation: Observation | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    observationMedia: ObservationMedia | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    organizer: Organizer | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    procedure: Procedure | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    regionOfInterest: RegionOfInterest | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    substanceAdministration: SubstanceAdministration | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    supply: Supply | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )

    @model_validator(mode="after")
    def organizer_only_one(self):
        """SHALL have no more than one of act, encounter, observation, observationMedia, organizer, procedure, regionOfInterest, substanceAdministration, or supply."""
        count = 0
        if self.act is not None:
            count += 1
        if self.observation is not None:
            count += 1
        if self.observationMedia is not None:
            count += 1
        if self.organizer is not None:
            count += 1
        if self.procedure is not None:
            count += 1
        if self.regionOfInterest is not None:
            count += 1
        if self.substanceAdministration is not None:
            count += 1
        if self.supply is not None:
            count += 1
        if count > 1:
            raise ValueError(
                "SHALL have no more than one of act, encounter, observation, observationMedia, "
                "organizer, procedure, regionOfInterest, substanceAdministration, or supply.."
            )
        return self
