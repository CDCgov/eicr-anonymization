"""ValueSet: ActMood.

https://terminology.hl7.org/5.2.0/ValueSet-v3-ActMood.html
"""

from enum import StrEnum


class ActMood(StrEnum):
    """ValueSet: ActMood.

    https://terminology.hl7.org/5.2.0/ValueSet-v3-ActMood.html
    """

    _ActMoodCompletionTrack = "_ActMoodCompletionTrack"
    _ActMoodPotential = "_ActMoodPotential"
    DEF = "DEF"
    PERM = "PERM"
    SLOT = "SLOT"
    EVN = "EVN"
    INT = "INT"
    _ActMoodDesire = "_ActMoodDesire"
    _ActMoodActRequest = "_ActMoodActRequest"
    ARQ = "ARQ"
    PERMRQ = "PERMRQ"
    RQO = "RQO"
    ORD = "ORD"
    PRP = "PRP"
    RMD = "RMD"
    PRMS = "PRMS"
    APT = "APT"
    _ActMoodPredicate = "_ActMoodPredicate"
    CRT = "CRT"
    EVN_CRT = "EVN.CRT"
    GOL_CRT = "GOL.CRT"
    INT_CRT = "INT.CRT"
    PRMS_CRT = "PRMS.CRT"
    RQO_CRT = "RQO.CRT"
    RSK_CRT = "RSK.CRT"
    EXPEC = "EXPEC"
    GOL = "GOL"
    RSK = "RSK"
    OPT = "OPT"
