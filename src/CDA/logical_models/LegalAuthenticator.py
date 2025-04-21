from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AssignedEntity import AssignedEntity
from CDA.logical_models.CS import CS
from CDA.logical_models.ED import ED
from CDA.logical_models.II import II
from CDA.logical_models.TS import TS
from CDA.value_sets.NullFlavor import NullFlavor


class LegalAuthenticator(BaseModel):
    """Logical Model: LegalAuthenticator (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-LegalAuthenticator.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["LA"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "LA",
        }
    )
    contextControlCode: Literal["OP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ContextControl",
            "binding_strength": "required",
            "fixed_value": "OP",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    time: TS = Field(json_schema_extra={"xml_type": "element"})
    signatureCode: CS = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    signatureText: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    assignedEntity: AssignedEntity = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
