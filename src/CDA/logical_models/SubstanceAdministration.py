from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import bl, cs
from CDA.logical_models.Author import Author
from CDA.logical_models.CD import CD
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.ED import ED
from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.EntryRelationship import EntryRelationship
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.IVL_INT import IVL_INT
from CDA.logical_models.IVL_PQ import IVL_PQ
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.ManufacturedProduct import ManufacturedProduct
from CDA.logical_models.Participant2 import Participant2
from CDA.logical_models.Performer2 import Performer2
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.Precondition import Precondition
from CDA.logical_models.Reference import Reference
from CDA.logical_models.RTO_PQ_PQ import RTO_PQ_PQ
from CDA.logical_models.Specimen import Specimen
from CDA.logical_models.Subject import Subject
from CDA.logical_models.SXCM_TS import SXCM_TS
from CDA.logical_models.SXPR_TS import SXPR_TS


class _consumable(InfrastructureRoot):
    """Specialized model of InfrastructureRoot for substanceAdministration."""

    typeCode: Literal["CSM"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationTargetDirect",
            "binding_strength": "required",
            "fixed_value": "CSM",
        }
    )
    manufacturedProduct: ManufacturedProduct = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )


class SubstanceAdministration(BaseModel):
    """Logical Model: SubstanceAdministration (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SubstanceAdministration.html
    """

    classCode: Literal["SBADM"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClassObservation",
            "binding_strength": "required",
            "fixed_value": "SBADM",
        }
    )
    moodCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMood",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        },
    )
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ActSubstanceAdministrationCode",
            "binding_strength": "extensible",
        }
    )
    negationInd: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
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
    effectiveTime: list[SXCM_TS | IVL_TS | EIVL_TS | PIVL_TS | SXPR_TS] | None = Field(
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
    routeCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "RouteOfAdministration",
            "binding_strength": "extensible",
        }
    )
    approachSiteCode: list[CD] | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Value Set ActSite",
            "binding_strength": "extensible",
        }
    )
    doseQuantity: IVL_PQ | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    rateQuantity: IVL_PQ | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    maxDoseQuantity: RTO_PQ_PQ | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    administrationUnitCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "AdministrableDrugForm",
            "binding_strength": "extensible",
        }
    )
    consumable: _consumable = Field(
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
