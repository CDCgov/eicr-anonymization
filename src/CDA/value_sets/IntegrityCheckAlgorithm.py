"""IntegrityCheckAlgorithm.

https://terminology.hl7.org/5.2.0/ValueSet-v3-IntegrityCheckAlgorithm.html
"""

from enum import StrEnum


class IntegrityCheckAlgorithm(StrEnum):
    """IntegrityCheckAlgorithm.

    https://terminology.hl7.org/5.2.0/ValueSet-v3-IntegrityCheckAlgorithm.html
    """

    SHA1 = "SHA-1"
    SHA256 = "SHA-256"
