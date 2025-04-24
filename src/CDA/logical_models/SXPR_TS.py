"""Logical Model: SXPR_TS: Component part of GTS (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXPR-TS.html
"""

from pydantic import Field

from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.SXCM_TS import SXCM_TS


class SXPR_TS(SXCM_TS):
    """Logical Model: SXPR_TS: Component part of GTS (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-SXPR-TS.html
    """

    comps: "list[SXCM_TS | IVL_TS | EIVL_TS | PIVL_TS | SXPR_TS] | None" = Field(
        json_schema_extra={"xml_type": "element"}, min_length=2
    )
