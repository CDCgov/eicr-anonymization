from pydantic import Field

from CDA.logical_models.PQ import PQ
from CDA.logical_models.QTY import QTY


class RTO_PQ_PQ(QTY):
    """Logical Model: RTO_PQ_PQ: Ratio (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RTO-PQ-PQ.html
    """

    numerator: PQ = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    denominator: PQ = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
