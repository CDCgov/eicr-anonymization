from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.LabeledDrug import LabeledDrug
from CDA.logical_models.Material import Material
from CDA.logical_models.Organization import Organization


class ManufacturedProduct(BaseModel):
    """Logical Model: ManufacturedProduct (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ManufacturedProduct.html
    """

    classCode: Literal["MANU"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassManufacturedProduct",
            "binding_strength": "required",
            "fixed_value": "MANU",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        },
    )
    identifiedBy: list[IdentifiedBy] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    manufacturedLabeledDrug: list[LabeledDrug] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    manufacturedMaterial: Material | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    manufacturerOrganization: list[Organization] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
