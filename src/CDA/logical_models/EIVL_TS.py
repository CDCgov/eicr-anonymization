"""Logical Model: EIVL_TS: EventRelatedPeriodicInterval (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-TS.html
"""

from typing import Literal

from pydantic import Field

from CDA.logical_models.CE import CE
from CDA.logical_models.IVL_PQ import IVL_PQ
from CDA.logical_models.SXCM_TS import SXCM_TS


class EIVL_TS(SXCM_TS):
    """Logical Model: EIVL_TS: EventRelatedPeriodicInterval (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-EIVL-TS.html
    """

    value: Literal[None] = None
    event: CE | None = Field(json_schema_extra={"xml_type": "element"})
    offset: IVL_PQ | None = Field(json_schema_extra={"xml_type": "element"})
