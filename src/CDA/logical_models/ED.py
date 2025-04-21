"""EncapsulatedData.

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ED.html
"""

from pydantic import BaseModel, Field, model_validator

from CDA.data_types.string_validators import bin, cs, st
from CDA.logical_models.TEL import TEL
from CDA.value_sets.CompressionAlgorithm import CompressionAlgorithm
from CDA.value_sets.IntegrityCheckAlgorithm import IntegrityCheckAlgorithm


class ED(BaseModel):
    """Encapsulated data."""

    charset: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    compression: CompressionAlgorithm | None = Field(json_schema_extra={"xml_type": "attribute"})
    integrityCheck: bin | None = Field(json_schema_extra={"xml_type": "attribute"})
    integrityCheckAlgorithm: IntegrityCheckAlgorithm | None = Field(
        json_schema_extra={"xml_type": "attribute"}
    )
    language: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    mediaType: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    representation: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    dataString: st | None = Field(json_schema_extra={"xml_type": "element"})
    dataBase64Binary: bin | None = Field(json_schema_extra={"xml_type": "element"})
    reference: TEL | None = Field(
        default=None,
        json_schema_extra={"xml_type": "element"},
    )
    thumbnail: "ED | None" = Field(
        default=None,
        json_schema_extra={"xml_type": "element"},
    )

    @model_validator(mode="after")
    def validate_data_fields(self) -> "ED":
        """Ensure that only one of dataString or dataBase64Binary is set."""
        if self.dataString is not None and self.dataBase64Binary is not None:
            raise DataFieldsException()
        return self


class DataFieldsException(ValueError):
    """Exception raised when both dataString and dataBase64Binary are set."""

    def __init__(self, message: str = "Only one of dataString or dataBase64Binary can be set"):
        """Initialize the custom exception with a message."""
        super().__init__(message)
