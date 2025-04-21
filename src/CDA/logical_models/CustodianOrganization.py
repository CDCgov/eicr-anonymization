"""Logical Model: CustodianOrganization (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CustodianOrganization.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.AD import AD
from CDA.logical_models.II import II
from CDA.logical_models.ON import ON
from CDA.logical_models.TEL import TEL


class CustodianOrganization(BaseModel):
    """Logical Model: CustodianOrganization (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CustodianOrganization.html
    """

    classCode: Literal["ORG"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassOrganization",
            "binding_strength": "required",
            "fixed_value": "ORG",
        }
    )
    determinerCode: Literal["INSTANCE"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityDeterminer",
            "binding_strength": "required",
            "fixed_value": "INSTANCE",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] = Field(
        min_length=1,
        json_schema_extra={
            "xml_type": "element",
        },
    )
    name: ON | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    telecom: TEL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    addr: AD | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
