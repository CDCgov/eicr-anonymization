"""CompressionAlgorithm.

https://terminology.hl7.org/5.2.0/ValueSet-v3-CompressionAlgorithm.html
"""
from enum import StrEnum


class CompressionAlgorithm(StrEnum):
    """CompressionAlgorithm."""

    BZ = "BZ"
    DF = "DF"
    GZ = "GZ"
    Z = "Z"
    Z7 = "Z7"
    ZL = "ZL"
