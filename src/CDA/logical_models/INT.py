"""Logical Model: INT: IntegerNumber (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-INT.html.
"""

from pydantic import Field

from CDA.data_types.string_validators import int as int_validator
from CDA.logical_models.QTY import QTY


class INT(QTY):
    """Logical Model: INT: IntegerNumber (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-INT.html.
    """

    value: int_validator | None = Field(json_schema_extra={"xml_type": "attribute"})
