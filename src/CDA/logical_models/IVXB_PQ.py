"""Logical Model: IVXB_PQ: Interval Boundary PhysicalQuantity (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-PQ.html
"""

from pydantic import Field

from CDA.data_types.string_validators import bl
from CDA.logical_models.PQ import PQ


class IVXB_PQ(PQ):
    """Logical Model: IVXB_PQ: Interval Boundary PhysicalQuantity (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-PQ.html
    """

    inclusive: bl | None = Field(json_schema_extra={"xml_type": "attribute"})
