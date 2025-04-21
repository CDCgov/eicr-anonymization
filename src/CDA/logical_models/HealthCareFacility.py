from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CE import CE
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.Organization import Organization
from CDA.logical_models.Place import Place


class HealthCareFacility(BaseModel):
    """Logical Model: HealthCareFacility (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-HealthCareFacility.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassServiceDeliveryLocation",
            "binding_strength": "required",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    identifiedBy: list[IdentifiedBy] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "ServiceDeliveryLocationRoleType",
            "binding_strength": "extensible",
        }
    )
    location: Place | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    serviceProviderOrganization: Organization | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
