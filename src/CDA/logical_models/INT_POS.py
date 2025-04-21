"""INT_POS: Positive integer numbers (V3 Data Type) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-INT-POS.html
"""

from pydantic import model_validator

from CDA.logical_models.INT import INT


class INT_POS(INT):
    """INT_POS: Positive integer numbers (V3 Data Type) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-INT-POS.html
    """

    @model_validator(mode="after")
    def _positive(self):
        """Check if the value is a positive integer."""
        if self.value and int(self.value) <= 0:
            raise ValueError("Value must be a positive integer.")
        return self
