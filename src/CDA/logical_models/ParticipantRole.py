from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AD import AD
from CDA.logical_models.CE import CE
from CDA.logical_models.Device import Device
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.TEL import TEL


class ParticipantRole(BaseModel):
    """Logical Model: ParticipantRole (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ParticipantRole.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassRoot",
            "binding_strength": "required",
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
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System RoleCode",
            "binding_strength": "extensible",
        }
    )
    addr: list[AD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    playingDevice: Device | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
