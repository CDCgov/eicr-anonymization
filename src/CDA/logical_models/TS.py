"""Logical Model: TS: PointInTime (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-TS.html
"""

from pydantic import Field

from CDA.data_types.string_validators import ts
from CDA.logical_models.ANY import ANY


class TS(ANY):
    """Logical Model: TS: PointInTime (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-TS.html
    """

    value: ts | None = Field(json_schema_extra={"xml_type": "attribute"})
