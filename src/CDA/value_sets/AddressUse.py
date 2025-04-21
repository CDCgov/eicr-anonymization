"""ValueSet: AddressUse.

https://terminology.hl7.org/5.2.0/ValueSet-v3-AddressUse.html
"""

from enum import StrEnum


class AddressUse(StrEnum):
    """ValueSet: AddressUse.

    https://terminology.hl7.org/5.2.0/ValueSet-v3-AddressUse.html
    """

    _GeneralAddressUse = "_GeneralAddressUse"
    BAD = "BAD"
    CONF = "CONF"
    H = "H"
    HP = "HP"
    HV = "HV"
    OLD = "OLD"
    TMP = "TMP"
    WP = "WP"
    DIR = "DIR"
    PUB = "PUB"
    _PostalAddressUse = "_PostalAddressUse"
    PHYS = "PHYS"
    PST = "PST"
    _TelecommunicationAddressUse = "_TelecommunicationAddressUse"
    AS = "AS"
    EC = "EC"
    MC = "MC"
    PG = "PG"
