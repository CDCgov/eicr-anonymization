"""Logical Model: ANY: DataValue (V3 Data Type) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ANY.html
"""

from pydantic import BaseModel, Field

from CDA.value_sets.NullFlavor import NullFlavor


class ANY(BaseModel):
    """Logical Model: ANY: DataValue (V3 Data Type) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ANY.html
    """

    nullFlavor: NullFlavor | None = Field(json_schema_extra={"xml_type": "attribute"})
