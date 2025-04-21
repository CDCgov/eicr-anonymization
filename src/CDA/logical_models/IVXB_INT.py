from pydantic import Field

from CDA.data_types.string_validators import bl
from CDA.logical_models.INT import INT


class IVXB_INT(INT):
    """Logical Model: IVXB_INT: Interval Boundary IntegerNumber (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-IVXB-INT.html
    """

    inclusive: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
        }
    )
