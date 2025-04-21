from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import bl, cs
from CDA.logical_models.AD import AD
from CDA.logical_models.ANY import ANY
from CDA.logical_models.Author import Author
from CDA.logical_models.BL import BL
from CDA.logical_models.CD import CD
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.CV import CV
from CDA.logical_models.ED import ED
from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.EN import EN
from CDA.logical_models.EntryRelationship import EntryRelationship
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.INT import INT
from CDA.logical_models.IVL_INT import IVL_INT
from CDA.logical_models.IVL_PQ import IVL_PQ
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.MO import MO
from CDA.logical_models.Participant2 import Participant2
from CDA.logical_models.Performer2 import Performer2
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.PQ import PQ
from CDA.logical_models.Precondition import Precondition
from CDA.logical_models.REAL import REAL
from CDA.logical_models.Reference import Reference
from CDA.logical_models.RTO_PQ_PQ import RTO_PQ_PQ
from CDA.logical_models.SC import SC
from CDA.logical_models.Specimen import Specimen
from CDA.logical_models.ST import ST
from CDA.logical_models.Subject import Subject
from CDA.logical_models.SXPR_TS import SXPR_TS
from CDA.logical_models.TEL import TEL
from CDA.logical_models.TS import TS


class _referenceRange(InfrastructureRoot):
    """Specialized model of infrastructureRoot for referenceRange."""

    typeCode: Literal["REFV"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActRelationshipPertains",
            "binding_strength": "required",
            "fixed_value": "REFV",
        }
    )


class Observation(BaseModel):
    """Logical Model: Observation (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Observation.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClassObservation",
            "binding_strength": "required",
        }
    )
    moodCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    negationInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ObservationType",
            "binding_strength": "extensible",
        }
    )
    derivationExpr: ST | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    text: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    statusCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActStatus",
            "binding_strength": "required",
        }
    )
    effectiveTime: IVL_TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    priorityCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActPriority",
            "binding_strength": "extensible",
        }
    )
    repeatNumber: IVL_INT | None = Field(
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
    value: (
        list[
            ANY
            | BL
            | ED
            | ST
            | CD
            | CV
            | CE
            | SC
            | II
            | TEL
            | AD
            | EN
            | INT
            | REAL
            | PQ
            | MO
            | TS
            | IVL_PQ
            | IVL_TS
            | PIVL_TS
            | EIVL_TS
            | SXPR_TS
            | RTO_PQ_PQ
        ]
        | None
    ) = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    interpretationCode: list[CE] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ObservationInterpretation",
            "binding_strength": "required",
        }
    )
    methodCode: list[CE] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ObservationMethod",
            "binding_strength": "extensible",
        }
    )
    targetSiteCode: list[CD] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    subject: Subject | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    specimen: list[Specimen] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    performer: list[Performer2] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    author: list[Author] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    informant: list[Informant] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    participant: list[Participant2] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    entryRelationship: list[EntryRelationship] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    reference: list[Reference] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    precondition: list[Precondition] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    referenceRange: list[_referenceRange] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
