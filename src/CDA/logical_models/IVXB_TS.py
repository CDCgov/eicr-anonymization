"""Logical Model: IVXB_TS: Interval Boundary PointInTime (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-TS.html
"""


from pydantic import Field

from CDA.data_types.string_validators import bl
from CDA.logical_models.TS import TS


class IVXB_TS(TS):
    """Logical Model: IVXB_TS: Interval Boundary PointInTime (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-TS.html
    """

    inclusive: bl | None = Field(
        json_schema_extra={"xml_type": "attribute"}
    )
