from pydantic import Field, model_validator

from CDA.data_types.string_validators import cs, int
from CDA.logical_models.ANY import ANY
from CDA.logical_models.INT import INT
from CDA.logical_models.IVXB_INT import IVXB_INT


class IVL_INT(ANY):
    """Logical Model: IVL_INT: Interval (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVL-INT.html
    """

    value: int | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
    operator: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "SetOperator",
            "binding_strength": "required",
        }
    )
    low: IVXB_INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    center: INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    width: INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    high: IVXB_INT | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )

    @model_validator(mode="after")
    def ivl_int_center(self):
        """Center cannot co-exist with low or high."""
        if self.center and (self.low or self.high):
            raise ValueError("Center cannot co-exist with low or high")
        return self
