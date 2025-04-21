"""Logical Model: CS: CodedSimpleValue (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CS.html
"""

from typing import Literal

from CDA.logical_models.CV import CV


class CS(CV):
    """Logical Model: CS: CodedSimpleValue (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CS.html
    """

    codeSystem: Literal[None] = None
    codeSystemName: Literal[None] = None
    codeSystemVersion: Literal[None] = None
    displayName: Literal[None] = None
    originalText: Literal[None] = None
