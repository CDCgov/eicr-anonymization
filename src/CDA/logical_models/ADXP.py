"""Logical Model: ADXP: CharacterString (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ADXP.html
"""

from pydantic import Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.ST import ST


class ADXP(ST):
    """Logical Model: ADXP: CharacterString (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ADXP.html
    """

    partType: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
