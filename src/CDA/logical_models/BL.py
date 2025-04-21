"""Logical Model: BL: Boolean (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-BL.html
"""

from pydantic import Field

from CDA.data_types.string_validators import bl
from CDA.logical_models.ANY import ANY


class BL(ANY):
    """Logical Model: BL: Boolean (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-BL.html
    """

    value: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
