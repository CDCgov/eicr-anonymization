"""Logical Model: CE: CodedWithEquivalents (V3 Data Type) .

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CE.html
"""



from typing import Literal

from CDA.logical_models.CD import CD


class CE(CD):
    """Logical Model: CE: CodedWithEquivalents (V3 Data Type) .

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-CE.html
    """

    qualifier: Literal[None] = None
