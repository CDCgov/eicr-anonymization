"""Logical Model: PN: PersonName (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PN.html
"""

from CDA.logical_models.EN import EN


class PN(EN):
    """Logical Model: PN: PersonName (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-PN.html
    """

    def pn_no_ls(self):
        """No PN name part may have a qualifier of LS."""
        if (
            (self.delimiter and any(part.qualifier == "LS" for part in self.delimiter))
            or (self.family and any(part.qualifier == "LS" for part in self.family))
            or (self.given and any(part.qualifier == "LS" for part in self.given))
            or (self.prefix and any(part.qualifier == "LS" for part in self.prefix))
            or (self.suffix and any(part.qualifier == "LS" for part in self.suffix))
        ):
            raise ValueError("No PN name part may have a qualifier of LS.")
