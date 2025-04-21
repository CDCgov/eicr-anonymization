from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.Consent import Consent
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.value_sets.NullFlavor import NullFlavor


class Authorization(BaseModel):
    """Logical Model: Authorization (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Authorization.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["AUTH"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "AUTH",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    consent: Consent = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
