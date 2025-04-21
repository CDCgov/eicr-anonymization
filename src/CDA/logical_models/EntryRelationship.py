from pydantic import Field, model_validator

from CDA.data_types.string_validators import bl, cs
from CDA.logical_models.Act import Act
from CDA.logical_models.BL import BL
from CDA.logical_models.Encounter import Encounter
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.INT import INT
from CDA.logical_models.Observation import Observation
from CDA.logical_models.ObservationMedia import ObservationMedia
from CDA.logical_models.Organizer import Organizer
from CDA.logical_models.Procedure import Procedure
from CDA.logical_models.RegionOfInterest import RegionOfInterest
from CDA.logical_models.SubstanceAdministration import SubstanceAdministration
from CDA.logical_models.Supply import Supply


class EntryRelationship(InfrastructureRoot):
    """Logical Model: EntryRelationship (CDA Class) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EntryRelationship.html
    """

    typeCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "x_ActRelationshipEntryRelationship",
            "binding_strength": "required",
        }
    )
    inversionInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    contextConductionInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    negationInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    sequenceNumber: INT | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    seperatableInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    act: Act | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    encounter: Encounter | None = Field(
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
    def entry_rel_only_one(self):
        """Ensure that only one of the entry relationship elements is present."""
        entry_relationship_elements = [
            self.act,
            self.encounter,
            self.observation,
            self.observationMedia,
            self.organizer,
            self.procedure,
            self.regionOfInterest,
            self.substanceAdministration,
            self.supply,
        ]
        if sum([1 for element in entry_relationship_elements if element is not None]) > 1:
            raise ValueError(
                "HALL have no more than one of act, encounter, observation, "
                "observationMedia, organizer, procedure, regionOfInterest, "
                "substanceAdministration, or supply."
            )
        return self
