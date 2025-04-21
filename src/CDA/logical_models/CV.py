"""Logical Model: CV: CodedValue (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CV.html
"""



from typing import Literal

from CDA.logical_models.CE import CE


class CV(CE):
    """Logical Model: CV: CodedValue (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CV.html
    """

    translation: Literal[None] = None
