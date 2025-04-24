"""Logical Model: CD: ConceptDescriptor (V3 Data Type) ."""

from typing import TYPE_CHECKING

from pydantic import Field

from CDA.data_types.string_validators import cs, oid, ruid, st, uuid
from CDA.logical_models.ANY import ANY
from CDA.logical_models.ED import ED

if TYPE_CHECKING:
    from CDA.logical_models.CR import CR


class CD(ANY):
    """Concept descriptor.

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CD.html
    """

    code: cs | None = Field(default=None, json_schema_extra={"xml_type": "element"})
    codeSystem: oid | uuid | ruid | None = Field(
        default=None, json_schema_extra={"xml_type": "attribute"}
    )
    codeSystemName: st | None = Field(default=None, json_schema_extra={"xml_type": "attribute"})
    codeSystemVersion: st | None = Field(default=None, json_schema_extra={"xml_type": "attribute"})
    displayName: st | None = Field(default=None, json_schema_extra={"xml_type": "attribute"})
    valueSet: oid | None = Field(default=None, json_schema_extra={"xml_type": "attribute"})
    valueSetVersion: st | None = Field(default=None, json_schema_extra={"xml_type": "attribute"})
    orginalText: ED | None = Field(default=None, json_schema_extra={"xml_type": "element"})

    # Use CR from TYPE_CHECKING import
    qualifier: "list[CR] | None" = Field(
        default=None,
        json_schema_extra={"xml_type": "element"},
    )

    # Self-reference is okay with postponed annotations
    translation: "list[CD] | None" = Field(
        default=None,
        json_schema_extra={"xml_type": "element"},
    )
