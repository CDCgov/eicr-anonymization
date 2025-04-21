"""Interval.

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-TS.html
"""

from pydantic import Field, model_validator

from CDA.logical_models.IVXB_TS import IVXB_TS
from CDA.logical_models.PQ import PQ
from CDA.logical_models.SXCM_TS import SXCM_TS
from CDA.logical_models.TS import TS


class IVL_TS(SXCM_TS):
    """Logical Model: IVL_TS: Interval (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-TS.html
    """

    low: IVXB_TS | None = Field(json_schema_extra={"xml_type": "element"})
    center: TS | None = Field(json_schema_extra={"xml_type": "element"})
    width: PQ | None = Field(json_schema_extra={"xml_type": "element"})
    high: IVXB_TS | None = Field(json_schema_extra={"xml_type": "element"})

    @model_validator(mode="after")
    def ivl_ts_center(self) -> "IVL_TS":
        """ivl-ts-center: Center cannot co-exist with low or high."""
        if self.center is not None and (self.low is not None or self.high is not None):
            raise ivl_ts_center_exception
        return self


class ivl_ts_center_exception(ValueError):
    """Custom exception for IVL_TS center validation."""

    def __init__(self, message: str = "ivl-ts-center: Center cannot co-exist with low or high"):
        """Initialize the custom exception with a message."""
        super().__init__(message)
