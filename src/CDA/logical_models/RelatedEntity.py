"""Logical Model: RelatedEntity (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedEntity.html
"""

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AD import AD
from CDA.logical_models.CE import CE
from CDA.logical_models.II import II
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.Person import Person
from CDA.logical_models.TEL import TEL


class RelatedEntity(BaseModel):
    """Logical Model: RelatedEntity (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedEntity.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClassMutualRelationship",
            "binding_strength": "required",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "PErsonalRelationshipRoleType",
            "binding_strength": "extensible",
        }
    )
    addr: list[AD] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    telecom: list[TEL] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    effectiveTime: IVL_TS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    relatedPerson: Person | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
