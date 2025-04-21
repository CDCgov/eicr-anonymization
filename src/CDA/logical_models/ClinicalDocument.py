"""Logical Model: ClinicalDocument (CDA Class)."""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import st
from CDA.logical_models.Authenticator import Authenticator
from CDA.logical_models.Author import Author
from CDA.logical_models.Authorization import Authorization
from CDA.logical_models.CE import CE
from CDA.logical_models.Component import Component
from CDA.logical_models.ComponentOf import ComponentOf
from CDA.logical_models.CS import CS
from CDA.logical_models.Custodian import Custodian
from CDA.logical_models.DataEnterer import DataEnterer
from CDA.logical_models.DocumentationOf import DocumentationOf
from CDA.logical_models.II import II
from CDA.logical_models.Informant import Informant
from CDA.logical_models.InformationRecipient import InformationRecipient
from CDA.logical_models.InFulfillmentOf import InFulfillmentOf
from CDA.logical_models.INT import INT
from CDA.logical_models.LegalAuthenticator import LegalAuthenticator
from CDA.logical_models.Participant1 import Participant1
from CDA.logical_models.RecordTarget import RecordTarget
from CDA.logical_models.RelatedDocument import RelatedDocument
from CDA.logical_models.TS import TS
from CDA.value_sets.ActClass import ActClass
from CDA.value_sets.ActMood import ActMood


class _TypeId(II):
    """A specialized II for typeId to capture requirements from ClinicalDocument."""

    root: Literal["2.16.840.1.113883.1.3"] = Field(
        json_schema_extra={"xml_type": "attribute", "fixed_value": "2.16.840.1.113883.1.3"}
    )
    extension: st = Field(json_schema_extra={"xml_type": "attribute"})


class ClinicalDocument(BaseModel):
    """Logical Model: ClinicalDocument (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ClinicalDocument.html
    """

    classCode: Literal[ActClass.DOCCLIN] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClass",
            "binding_strength": "extensible",
            "fixed_value": ActClass.DOCCLIN,
        }
    )
    moodCode: Literal[ActMood.EVN] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMood",
            "binding_strength": "required",
            "fixed_value": ActMood.EVN,
        }
    )
    realmCode: CS | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: _TypeId = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: II = Field(json_schema_extra={"xml_type": "element"})
    code: CE = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "FHIRDocumentTypeCodes",
            "binding_strength": "extensible",
        }
    )
    title: st | None = Field(json_schema_extra={"xml_type": "element"})
    effectiveTime: TS = Field(json_schema_extra={"xml_type": "element"})
    confidentialityCode: CE = Field(json_schema_extra={"xml_type": "element"})
    languageCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "HumanLanguage",
            "binding_strength": "required",
        }
    )
    setId: II | None = Field(json_schema_extra={"xml_type": "element"})
    versionNumber: INT | None = Field(json_schema_extra={"xml_type": "element"})
    CopyTime: TS | None = Field(json_schema_extra={"xml_type": "element"})
    recordTarget: list[RecordTarget] = Field(
        json_schema_extra={"xml_type": "element"},
        min_length=1,
    )
    author: list[Author] = Field(
        json_schema_extra={"xml_type": "element"},
        min_length=1,
    )
    dataEnterer: DataEnterer | None = Field(json_schema_extra={"xml_type": "element"})
    informant: list[Informant] | None = Field(json_schema_extra={"xml_type": "element"})
    custodian: Custodian = Field(json_schema_extra={"xml_type": "element"})
    informationRecipient: list[InformationRecipient] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    legalAuthenticator: LegalAuthenticator | None = Field(json_schema_extra={"xml_type": "element"})
    authenticator: list[Authenticator] | None = Field(json_schema_extra={"xml_type": "element"})
    participant: list[Participant1] | None = Field(json_schema_extra={"xml_type": "element"})
    inFulfillmentOf: list[InFulfillmentOf] | None = Field(json_schema_extra={"xml_type": "element"})
    documentationOf: list[DocumentationOf] | None = Field(json_schema_extra={"xml_type": "element"})
    relatedDocument: list[RelatedDocument] | None = Field(json_schema_extra={"xml_type": "element"})
    authorization: list[Authorization] | None = Field(json_schema_extra={"xml_type": "element"})
    componentOf: ComponentOf | None = Field(json_schema_extra={"xml_type": "element"})
    component: Component = Field(json_schema_extra={"xml_type": "element"})
