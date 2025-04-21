from pydantic import Field

from CDA.data_types.string_validators import real
from CDA.logical_models.QTY import QTY


class REAL(QTY):
    """Logical Model: REAL: RealNumber (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-REAL.html
    """

    value: real | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
