"""Logical Model: SXCM_TS: GeneralTimingSpecification (V3 Data Type) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXCM-TS.html
"""

from pydantic import Field

from CDA.logical_models.TS import TS
from CDA.value_sets.SetOperator import SetOperator


class SXCM_TS(TS):
    """Logical Model: SXCM_TS: GeneralTimingSpecification (V3 Data Type) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXCM-TS.html
    """

    operator: SetOperator | None = Field(json_schema_extra={"xml_type": "attribute"})
