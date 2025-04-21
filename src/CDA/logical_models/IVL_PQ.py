"""Logical Model: IVL_PQ: Interval (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-PQ.html
"""

from pydantic import Field, model_validator

from CDA.data_types.string_validators import cs, real
from CDA.logical_models.ANY import ANY
from CDA.logical_models.IVXB_PQ import IVXB_PQ
from CDA.logical_models.PQ import PQ
from CDA.value_sets.SetOperator import SetOperator


class IVL_PQ(ANY):
    """Logical Model: IVL_PQ: Interval (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-PQ.html
    """

    unit: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    value: real | None = Field(json_schema_extra={"xml_type": "attribute"})
    operator: SetOperator | None = Field(json_schema_extra={"xml_type": "attribute"})
    low: IVXB_PQ | None = Field(json_schema_extra={"xml_type": "element"})
    center: PQ | None = Field(json_schema_extra={"xml_type": "element"})
    width: PQ | None = Field(json_schema_extra={"xml_type": "element"})
    high: IVXB_PQ | None = Field(json_schema_extra={"xml_type": "element"})

    @model_validator(mode="after")
    def ivl_pq_center(self) -> "IVL_PQ":
        """ivl-pq-center: Center cannot co-exist with low or high."""
        if self.center is not None and (self.low is not None or self.high is not None):
            raise ivl_pq_center_exception
        return self


class ivl_pq_center_exception(ValueError):
    """ivl-pq-center: Center cannot co-exist with low or high."""

    def __init__(self, message: str = "ivl-pq-center: Center cannot co-exist with low or high"):
        """Initialize the custom exception with a message."""
        super().__init__(message)
