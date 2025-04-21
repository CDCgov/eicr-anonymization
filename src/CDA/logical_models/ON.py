"""Logical Model: ON: OrganizationName (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ON.html
"""

from typing import Literal

from CDA.logical_models.EN import EN


class ON(EN):
    """Logical Model: ON: OrganizationName (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ON.html
    """

    family: Literal[None] = None
    given: Literal[None] = None
