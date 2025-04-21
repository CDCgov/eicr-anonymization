from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AD import AD
from CDA.logical_models.IdentifiedBy import IdentifiedBy
from CDA.logical_models.II import II
from CDA.logical_models.Organization import Organization
from CDA.logical_models.Person import Person
from CDA.logical_models.TEL import TEL


class IntendedRecipent(BaseModel):
    """Logical Model: IntendedRecipient (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IntendedRecipient.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    identifiedBy: list[IdentifiedBy] | None = Field(json_schema_extra={"xml_type": "element"})
    addr: list[AD] | None = Field(json_schema_extra={"xml_type": "element"})
    telecom: list[TEL] | None = Field(json_schema_extra={"xml_type": "element"})
    informationRecipient: Person | None = Field(json_schema_extra={"xml_type": "element"})
    receivedBy: Organization | None = Field(json_schema_extra={"xml_type": "element"})
