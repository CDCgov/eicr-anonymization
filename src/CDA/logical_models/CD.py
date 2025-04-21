"""Logical Model: CD: ConceptDescriptor (V3 Data Type) ."""

from pydantic import Field

from CDA.data_types.string_validators import cs, oid, ruid, st, uuid
from CDA.logical_models.ANY import ANY
from CDA.logical_models.CD import CD
from CDA.logical_models.CR import CR
from CDA.logical_models.ED import ED


class CD(ANY):
    """Concept descriptor.

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CD.html
    """

    code: cs | None = Field(json_schema_extra={"xml_type": "element"})
    codeSystem: oid | uuid | ruid | None = Field(json_schema_extra={"xml_type": "attribute"})
    codeSystemName: st | None = Field(json_schema_extra={"xml_type": "attribute"})
    codeSystemVersion: st | None = Field(json_schema_extra={"xml_type": "attribute"})
    displayName: st | None = Field(json_schema_extra={"xml_type": "attribute"})
    valueSet: oid | None = Field(json_schema_extra={"xml_type": "attribute"})
    valueSetVersion: st | None = Field(json_schema_extra={"xml_type": "attribute"})
    orginalText: ED | None = Field(json_schema_extra={"xml_type": "element"})
    qualifier: list[CR] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    translation: list[CD] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
