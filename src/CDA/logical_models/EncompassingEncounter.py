from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.CE import CE
from CDA.logical_models.EncounterParticipant import EncounterParticipant
from CDA.logical_models.HealthCareFacility import HealthCareFacility
from CDA.logical_models.II import II
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.value_sets.ActClass import ActClass
from CDA.value_sets.ActMood import ActMood


class _responsibleParty(InfrastructureRoot):
    """Specialized InfrastructureRoot for responsibleParty to capture requirements from EncompassingEncounter."""

    typeCode: Literal["RESP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationTargetLocation",
            "binding_strength": "required",
            "fixed_value": "RESP",
        }
    )
    assignedEntity: AssignedEntity = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )


class _location(InfrastructureRoot):
    """Specialized InfrastructureRoot for location to capture requirements from EncompassingEncounter."""

    typeCode: Literal["LOC"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationTargetLocation",
            "binding_strength": "required",
            "fixed_value": "LOC",
        }
    )
    healthCareFacility: HealthCareFacility = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )


class EncompassingEncounter(BaseModel):
    """Logical Model: EncompassingEncounter (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EncompassingEncounter.html
    """

    classCode: Literal[ActClass.ENC] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": ActClass.ENC,
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
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActEncounterCode",
            "binding_strength": "extensible",
        }
    )
    effectiveTime: IVL_TS = Field(json_schema_extra={"xml_type": "element"})
    admissionReferralSourceCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "USEncounterDischargeDisposition",
            "binding_strength": "extensible",
        }
    )
    responsibleParty: _responsibleParty | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    encounterParticipant: list[EncounterParticipant] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    location: _location | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
