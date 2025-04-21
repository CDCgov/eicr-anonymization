from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AD import AD
from CDA.logical_models.CE import CE
from CDA.logical_models.II import II
from CDA.logical_models.SubjectPerson import SubjectPerson
from CDA.logical_models.TEL import TEL


class RelatedSubject(BaseModel):
    """Logical Model: RelatedSubject (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedSubject.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "PersonalRelationshipRoleType",
            "binding_strength": "extensible",
        }
    )
    addr: list[AD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    subject: SubjectPerson | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
