"""Simple data types that can be defined by constraints on strings."""

from typing import Annotated

from pydantic import Field

bin = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?",
        description="Data Type Profile: bin: Binary Data",
    ),
]
"""Data Type Profile: bin: Binary Data
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-bin.html
"""
bl = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^true|false$",
        description="Data Type Profile: bl: Boolean",
    ),
]
"""Data Type Profile: bl: Boolean
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-bl-simple.html
"""
bn = Annotated[
    str,
    Field(
        default=None,
        pattern=r"^true|false$",
        description="Data Type Profile: bn: BooleanNonNull",
    ),
]
"""Data Type Profile: bn: BooleanNonNull
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-bn.html
"""
cs = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[A-Za-z0-9\\-]+$",
        description="Data Type Profile: cs: Coded Simple Value",
    ),
]
"""Data Type Profile: cs: Coded Simple Value
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-cs-simple.html
"""
id = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[A-Za-z0-9\-\.]{1,64}$",
        description="Data Type Profile: xs:ID",
    ),
]
"""Data Type Profile: xs:ID
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-xs-ID.html
"""
int = Annotated[
    str,
    Field(
        default=None,
        pattern=r"^[0]|[-+]?[1-9][0-9]*$",
        description="Data Type Profile: int: Integer Number",
    ),
]
"""Data Type Profile: int: Integer Number
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-int-simple.html
"""
oid = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[0-2](\.(0|[1-9][0-9]*))+$",
        description="Data Type Profile: oid: ISO Object Identifier",
    ),
]
"""Data Type Profile: oid: ISO Object Identifier
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-oid.html
"""
real = Annotated[
    str,
    Field(
        default=None,
        pattern=r"^[-+]?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$",
        description="Data Type Profile: real: Real Number",
    ),
]
"""Data Type Profile: real: Real Number
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-real-simple.html
"""
ruid = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[A-Za-z][A-Za-z0-9\\-]*$",
        description="Data Type Profile: ruid: Relative Unique Identifier",
    ),
]
""" Data Type Profile: ruid: Relative Unique Identifier
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ruid.html
"""
st = Annotated[
    str,
    Field(
        default=None,
        pattern=r"^[\r\n\t\u0020-\uFFFF]*$",
        description="Data Type Profile: st: String",
    ),
]
"""Data Type Profile: st: String
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-st-simple.html"""
ts = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[0-9]{1,8}|([0-9]{9,14}|[0-9]{14,14}\\.[0-9]+)([+-][0-9]{1,4})?$",
        description="Data Type Profile: ts: Point in Time",
    ),
]
""" Data Type Profile: ts: Point in Time
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ts-simple.html
"""
url = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"\S*",
        description="Data Type Profile: url: Uniform Resource Locator",
    ),
]
"""Data Type Profile: url: Uniform Resource Locator
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-url.html
"""
uuid = Annotated[
    str | None,
    Field(
        default=None,
        pattern=r"^[0-9A-Z]{8}-[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{12}$",
        description="Data Type Profile: uuid: Universally Unique Identifier",
    ),
]
"""Data Type Profile: uuid: Universally Unique Identifier
https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-uuid.html
"""
