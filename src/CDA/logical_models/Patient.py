"""Logical Model: Patient (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Patient.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.Birthplace import Birthplace
from CDA.logical_models.BL import BL
from CDA.logical_models.CE import CE
from CDA.logical_models.ED import ED
from CDA.logical_models.Guardian import Guardian
from CDA.logical_models.II import II
from CDA.logical_models.INT_POS import INT_POS
from CDA.logical_models.LanguageCommunication import LanguageCommunication
from CDA.logical_models.PN import PN
from CDA.logical_models.TS import TS


class Patient(BaseModel):
    """Logical Model: Patient (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Patient.html
    """

    classCode: Literal["PSN"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassLivingSubject",
            "binding_strength": "required",
            "fixed_value": "PSN",
        }
    )
    determinerCode: Literal["INSTANCE"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityDeterminer",
            "binding_strength": "required",
            "fixed_value": "INSTANCE",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    id: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    name: list[PN] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    desc: ED | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    administrativeGenderCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "AdministrativeGender",
            "binding_strength": "extensible",
        }
    )
    birthTime: TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    deceasedInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    deceasedTime: TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    multipleBirthInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    multipleBirthOrderNumber: INT_POS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    martialStatusCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "MaritalStatus",
            "binding_strength": "extensible",
        }
    )
    religiousAffiliationCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ReligiousAffiliation",
            "binding_strength": "extensible",
        }
    )
    raceCode: list[CE] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "Race",
            "binding_strength": "extensible",
        }
    )
    ethnicGroupCode: list[CE] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "Ethnicity",
            "binding_strength": "extensible",
        }
    )
    guardian: list[Guardian] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    birthplace: Birthplace | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    languageCommunication: list[LanguageCommunication] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
