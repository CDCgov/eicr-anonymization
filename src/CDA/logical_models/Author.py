"""Logical Model: Author (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Author.html
"""

from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AssignedAuthor import AssignedAuthor
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.TS import TS


class Author(BaseModel):
    """Logical Model: Author (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Author.html
    """

    nullFlavor: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: Literal["AUT"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationType",
            "binding_strength": "required",
            "fixed_value": "AUT",
        }
    )
    contextControlCode: Literal["OP"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ContextControl",
            "binding_strength": "required",
            "fixed_value": "OP",
        }
    )
    realmCode: list[CS] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    typeId: II | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    functionCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    time: TS = Field(
        json_schema_extra={"xml_type": "element"},
    )
    assignedAuthor: AssignedAuthor = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
