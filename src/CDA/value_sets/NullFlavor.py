"""ValueSet: NullFlavor.

https://terminology.hl7.org/5.2.0/ValueSet-v3-NullFlavor.html
"""

from enum import StrEnum


class NullFlavor(StrEnum):
    """ValueSet: NullFlavor.

    https://terminology.hl7.org/5.2.0/ValueSet-v3-NullFlavor.html
    """

    NI = "NI"
    INV = "INV"
    DER = "DER"
    OTH = "OTH"
    NINF = "NINF"
    PINF = "PINF"
    UNC = "UNC"
    MSK = "MSK"
    NA = "NA"
    UNK = "UNK"
    ASKU = "ASKU"
    NAV = "NAV"
    NASK = "NASK"
    NAVU = "NAVU"
    QS = "QS"
    TRC = "TRC"
    NP = "NP"
