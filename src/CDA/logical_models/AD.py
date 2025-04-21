"""Logical Model: AD: PostalAddress (V3 Data Type).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AD.html
"""

from typing import Literal

from pydantic import Field

from CDA.data_types.string_validators import bl, cs, st
from CDA.logical_models.ADXP import ADXP
from CDA.logical_models.ANY import ANY
from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.SXPR_TS import SXPR_TS
from CDA.value_sets.NullFlavor import NullFlavor


class _delimiter(ADXP):
    """A specialized ADXP for delimiter to capture requirements from AD."""

    partType: Literal["DEL"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DEL",
        }
    )


class _country(ADXP):
    """A specialized ADXP for country to capture requirements from AD."""

    partType: Literal["CNT"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "CNT",
        }
    )


class _state(ADXP):
    """A specialized ADXP for state to capture requirements from AD."""

    partType: Literal["STA"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "STA",
        }
    )


class _county(ADXP):
    """A specialized ADXP for county to capture requirements from AD."""

    partType: Literal["CPA"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "CPA",
        }
    )


class _city(ADXP):
    """A specialized ADXP for city to capture requirements from AD."""

    partType: Literal["CTY"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "CTY",
        }
    )


class _postalCode(ADXP):
    """A specialized ADXP for postalCode to capture requirements from AD."""

    partType: Literal["ZIP"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "ZIP",
        }
    )


class _streetAddressLine(ADXP):
    """A specialized ADXP for streetAddressLine to capture requirements from AD."""

    partType: Literal["SAL"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "SAL",
        }
    )


class _houseNumber(ADXP):
    """A specialized ADXP for houseNumber to capture requirements from AD."""

    partType: Literal["BNR"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "BNR",
        }
    )


class _houseNumberNumeric(ADXP):
    """A specialized ADXP for houseNumberNumeric to capture requirements from AD."""

    partType: Literal["BNN"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "BNN",
        }
    )


class _direction(ADXP):
    """A specialized ADXP for direction to capture requirements from AD."""

    partType: Literal["DIR"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DIR",
        }
    )


class _streetName(ADXP):
    """A specialized ADXP for streetName to capture requirements from AD."""

    partType: Literal["STR"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "STR",
        }
    )


class _streetNameBase(ADXP):
    """A specialized ADXP for streetNameBase to capture requirements from AD."""

    partType: Literal["STB"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "STB",
        }
    )


class _streetNameType(ADXP):
    """A specialized ADXP for streetNameType to capture requirements from AD."""

    partType: Literal["STTYP"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "STTYP",
        }
    )


class _additionalLocator(ADXP):
    """A specialized ADXP for additionalLocator to capture requirements from AD."""

    partType: Literal["ADL"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "ADL",
        }
    )


class _unitID(ADXP):
    """A specialized ADXP for unitID to capture requirements from AD."""

    partType: Literal["UNID"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "UNID",
        }
    )


class _unitType(ADXP):
    """A specialized ADXP for unitType to capture requirements from AD."""

    partType: Literal["UNIT"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "UNIT",
        }
    )


class _careOf(ADXP):
    """A specialized ADXP for careOf to capture requirements from AD."""

    partType: Literal["CAR"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "CAR",
        }
    )


class _censusTract(ADXP):
    """A specialized ADXP for censusTract to capture requirements from AD."""

    partType: Literal["CEN"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "CEN",
        }
    )


class _deliveryAddressLine(ADXP):
    """A specialized ADXP for deliveryAddressLine to capture requirements from AD."""

    partType: Literal["DAL"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DAL",
        }
    )


class _deliveryInstallationType(ADXP):
    """A specialized ADXP for deliveryInstallationType to capture requirements from AD."""

    partType: Literal["DINST"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DINST",
        }
    )


class _deliveryInstallationArea(ADXP):
    """A specialized ADXP for deliveryInstallationArea to capture requirements from AD."""

    partType: Literal["DINSTA"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DINSTA",
        }
    )


class _deliveryMode(ADXP):
    """A specialized ADXP for deliveryMode to capture requirements from AD."""

    partType: Literal["DMOD"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DMOD",
        }
    )


class _deliveryModeIdentifier(ADXP):
    """A specialized ADXP for deliveryModeIdentifier to capture requirements from AD."""

    partType: Literal["DMODID"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "DMODID",
        }
    )


class _buildingNumberSuffix(ADXP):
    """A specialized ADXP for buildingNumberSuffix to capture requirements from AD."""

    partType: Literal["BNS"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "BNS",
        }
    )


class _postBox(ADXP):
    """A specialized ADXP for postBox to capture requirements from AD."""

    partType: Literal["POB"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "POB",
        }
    )


class _precinct(ADXP):
    """A specialized ADXP for precinct to capture requirements from AD."""

    partType: Literal["PRE"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "fixed_value": "PRE",
        }
    )


class AD(ANY):
    """Logical Model: AD: PostalAddress (V3 Data Type).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-AD.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    isNotOrdered: bl | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "Boolean",
            "binding_strength": "required",
        },
    )
    use: cs | None = Field(json_schema_extra={"xml_type": "attribute"})
    delimiter: list[_delimiter] | None = Field(json_schema_extra={"xml_type": "element"})
    country: list[_country] | None = Field(json_schema_extra={"xml_type": "element"})
    state: list[_state] | None = Field(json_schema_extra={"xml_type": "element"})
    county: list[_county] | None = Field(json_schema_extra={"xml_type": "element"})
    city: list[_city] | None = Field(json_schema_extra={"xml_type": "element"})
    postalCode: list[_postalCode] | None = Field(json_schema_extra={"xml_type": "element"})
    streetAddressLine: list[_streetAddressLine] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    houseNumber: list[_houseNumber] | None = Field(json_schema_extra={"xml_type": "element"})
    houseNumberNumeric: list[_houseNumberNumeric] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    direction: list[_direction] | None = Field(json_schema_extra={"xml_type": "element"})
    streetName: list[_streetName] | None = Field(json_schema_extra={"xml_type": "element"})
    streetNameBase: list[_streetNameBase] | None = Field(json_schema_extra={"xml_type": "element"})
    streetNameType: list[_streetNameType] | None = Field(json_schema_extra={"xml_type": "element"})
    additionalLocator: list[_additionalLocator] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    unitID: list[_unitID] | None = Field(json_schema_extra={"xml_type": "element"})
    unitType: list[_unitType] | None = Field(json_schema_extra={"xml_type": "element"})
    careOf: list[_careOf] | None = Field(json_schema_extra={"xml_type": "element"})
    censusTract: list[_censusTract] | None = Field(json_schema_extra={"xml_type": "element"})
    deliveryAddressLine: list[_deliveryAddressLine] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    deliveryInstallationType: list[_deliveryInstallationType] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    deliveryInstallationArea: list[_deliveryInstallationArea] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    deliveryMode: list[_deliveryMode] | None = Field(json_schema_extra={"xml_type": "element"})
    deliveryModeIdentifier: list[_deliveryModeIdentifier] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    buildingNumberSuffix: list[_buildingNumberSuffix] | None = Field(
        json_schema_extra={"xml_type": "element"}
    )
    postBox: list[_postBox] | None = Field(json_schema_extra={"xml_type": "element"})
    precinct: list[_precinct] | None = Field(json_schema_extra={"xml_type": "element"})
    xmlText: st | None = Field(
        json_schema_extra={
            "xml_type": "text",
        }
    )
    useablePeriod: list[IVL_TS | EIVL_TS | PIVL_TS | SXPR_TS] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
