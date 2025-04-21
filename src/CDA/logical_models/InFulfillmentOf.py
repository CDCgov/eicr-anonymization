from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.Order import Order
from CDA.value_sets.NullFlavor import NullFlavor


class InFulfillmentOf(BaseModel):
    """Logical Model: InFulfillmentOf (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InFulfillmentOf.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["FLFS"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "FLFS",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    order: Order = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
