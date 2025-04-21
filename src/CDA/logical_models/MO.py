from pydantic import Field

from CDA.data_types.string_validators import real
from CDA.logical_models.CS import CS
from CDA.logical_models.QTY import QTY


class MO(QTY):
    """Logical Model: MO: MonetaryAmount (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-MO.html
    """

    currency: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    value: real | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
