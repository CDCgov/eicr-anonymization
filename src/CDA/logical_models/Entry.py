from typing import Literal

from pydantic import Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.Act import Act
from CDA.logical_models.Encounter import Encounter
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.Observation import Observation
from CDA.logical_models.ObservationMedia import ObservationMedia
from CDA.logical_models.Organizer import Organizer
from CDA.logical_models.Procedure import Procedure
from CDA.logical_models.RegionOfInterest import RegionOfInterest
from CDA.logical_models.SubstanceAdministration import SubstanceAdministration
from CDA.logical_models.Supply import Supply


class Entry(InfrastructureRoot):
    """Logical Model: Entry (CDA Class) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Entry.html
    """

    typeCode: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "x_ActRelationshipEntry",
            "binding_strength": "required",
        }
    )
    contextConductionInd: Literal["true"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "true",
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