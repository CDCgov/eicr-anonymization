"""Logical Model: II: InstanceIdentifier (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-II.html
"""

from pydantic import Field

from CDA.data_types.string_validators import bl, oid, ruid, st, uuid
from CDA.logical_models.ANY import ANY


class II(ANY):
    """Logical Model: II: InstanceIdentifier (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-II.html
    """

    assigningAuthorityName: st | None = Field(json_schema_extra={"xml_type": "attribute"})
    displayable: bl | None = Field(json_schema_extra={"xml_type": "attribute"})
    root: oid | uuid | ruid | None = Field(json_schema_extra={"xml_type": "attribute"})
    extension: st | None = Field(json_schema_extra={"xml_type": "attribute"})
