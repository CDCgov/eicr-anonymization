from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.ServiceEvent import ServiceEvent
from CDA.value_sets.NullFlavor import NullFlavor


class DocumentationOf(BaseModel):
    """Logical Model: DocumentationOf (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructPureDefinition-DocumentationOf.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["DOC"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "DOC",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    serviceEvent: ServiceEvent = Field(json_schema_extra={"xml_type": "element"})
