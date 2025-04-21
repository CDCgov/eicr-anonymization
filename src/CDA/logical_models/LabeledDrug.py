from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.EN import EN
from CDA.logical_models.II import II
from CDA.value_sets.NullFlavor import NullFlavor


class LabeledDrug(BaseModel):
    """Logical Model: LabeledDrug (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-LabeledDrug.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    classCode: Literal["MMAT"] = Field(
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
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "Drug Entity",
            "binding_strength": "extensible",
        }
    )
    name: EN | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
