from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CD import CD
from CDA.logical_models.EN import EN
from CDA.logical_models.II import II
from CDA.logical_models.ST import ST
from CDA.value_sets.NullFlavor import NullFlavor


class Material(BaseModel):
    """Logical Model: Material (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Material.html
    """

    classCode: Literal["MMAT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityClassManufacturedMaterial",
            "binding_strength": "required",
            "fixed_value": "MMAT",
        }
    )
    determinerCode: Literal["KIND"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "EntityDeterminerDetermined",
            "binding_strength": "required",
            "fixed_value": "KIND",
        }
    )
    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "MaterialEntityClassType",
            "binding_strength": "extensible",
        }
    )
    name: EN | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    lotNumberText: ST | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
