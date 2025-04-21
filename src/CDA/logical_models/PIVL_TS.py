"""Logical Model: PIVL_TS: PeriodicIntervalOfTime (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PIVL-TS.html
"""

from typing import Literal

from pydantic import Field

from CDA.data_types.string_validators import bl, cs
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.PQ import PQ
from CDA.logical_models.SXCM_TS import SXCM_TS


class PIVL_TS(SXCM_TS):
    """Logical Model: PIVL_TS: PeriodicIntervalOfTime (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PIVL-TS.html
    """

    value: Literal[None] = None
    phase: IVL_TS | None = Field(json_schema_extra={"xml_type": "element"})
    period: PQ | None = Field(json_schema_extra={"xml_type": "element"})
    alignment: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    institutionSpecified: bl | None = Field(json_schema_extra={"xml_type": "attribute"})
