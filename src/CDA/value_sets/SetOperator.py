"""ValueSet: SetOperator.

https://terminology.hl7.org/5.2.0/ValueSet-v3-SetOperator.html
"""

from enum import StrEnum


class SetOperator(StrEnum):
    """ValueSet: SetOperator.

    https://terminology.hl7.org/5.2.0/ValueSet-v3-SetOperator.html
    """

    _ValueSetOperator = "_ValueSetOperator"
    E = "E"
    I = "I"  # noqa: E741
    A = "A"
    H = "H"
    P = "P"
