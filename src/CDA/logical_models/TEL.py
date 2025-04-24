"""Logical Model: TEL: TelecommunicationAddress (V3 Data Type)."""
from pydantic import Field

from CDA.data_types.string_validators import url
from CDA.logical_models.ANY import ANY
from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.SXPR_TS import SXPR_TS
from CDA.value_sets.AddressUse import AddressUse


class TEL(ANY):
    """Logical Model: TEL: TelecommunicationAddress (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-TEL.html
    """

    value: url | None = Field(json_schema_extra={"xml_type": "attribute"})
    useablePeriods: list[IVL_TS | EIVL_TS | PIVL_TS | SXPR_TS] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    use: AddressUse | None = Field(json_schema_extra={"xml_type": "attribute"})
