from typing import Literal

from pydantic import BaseModel, Field

from CDA.logical_models.CE import CE
from CDA.logical_models.ED import ED
from CDA.logical_models.II import II
from CDA.logical_models.INT import INT
from CDA.value_sets.ActMood import ActMood


class ParentDocument(BaseModel):
    """Logical Model: ParentDocument (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ParentDocument.html
    """

    classCode: Literal["DOCCLIN"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "RoleClass",
            "binding_strength": "required",
            "fixed_value": "DOCCLIN",
        }
    )
    moodCode: Literal[ActMood.EVN] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMood",
            "binding_strength": "required",
            "fixed_value": ActMood.EVN,
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    id: list[II] = Field(json_schema_extra={"xml_type": "element"}, min_length=1)
    code: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "FHIRDocumentTypeCodes",
            "binding_strength": "extensible",
        }
    )
    text: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    setId: II | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    versionNumber: INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
