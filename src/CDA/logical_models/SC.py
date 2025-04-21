"""Logical Model: SC: CharacterStringWithCode (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SC.html
"""

from pydantic import Field

from CDA.data_types.string_validators import cs, oid, ruid, st, uuid
from CDA.logical_models.ST import ST


class SC(ST):
    """Logical Model: SC (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SC.html
    """

    code: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    codeSystem: oid | uuid | ruid | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    codeSystemName: st | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    codeSystemVersion: st | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    displayName: st | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
