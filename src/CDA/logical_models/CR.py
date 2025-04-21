"""Logical Model: CR: ConceptRole (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CR.html
"""

from pydantic import Field

from CDA.data_types.string_validators import bn
from CDA.logical_models.ANY import ANY
from CDA.logical_models.CD import CD
from CDA.logical_models.CV import CV


class CR(ANY):
    """Logical Model: CR: ConceptRole (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CR.html
    """

    inverted: bn | None = Field(json_schema_extra={"xml_type": "attribute"})
    name: CV | None = Field(json_schema_extra={"xml_type": "element"})
    value: CD | None = Field(json_schema_extra={"xml_type": "element"})
