"""Logical Model: PQ: PhysicalQuantity (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PQ.html
"""

from pydantic import Field

from CDA.data_types.string_validators import cs, real
from CDA.logical_models.PQR import PQR
from CDA.logical_models.QTY import QTY


class PQ(QTY):
    """Logical Model: PQ: PhysicalQuantity (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PQ.html
    """

    unit: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    value: real | None = Field(json_schema_extra={"xml_type": "attribute"})
    translations: list[PQR] | None = Field(json_schema_extra={"xml_type": "element"})
