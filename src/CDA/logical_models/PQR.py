"""Logical Model: PQR: PhysicalQuantityRepresentation (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PQR.html
"""

from pydantic import Field

from CDA.data_types.string_validators import real
from CDA.logical_models.CV import CV


class PQR(CV):
    """Logical Model: PQR: PhysicalQuantityRepresentation (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PQR.html
    """

    value: real | None = Field(json_schema_extra={"xml_type": "attribute"})
