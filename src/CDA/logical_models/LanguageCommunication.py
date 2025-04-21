"""Logical Model: LanguageCommunication (CDA Class).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-LanguageCommunication.html
"""

from pydantic import BaseModel, Field

from CDA.logical_models.BL import BL
from CDA.logical_models.CE import CE
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II


class LanguageCommunication(BaseModel):
    """Logical Model: LanguageCommunication (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-LanguageCommunication.html
    """

    templateId: list[II] | None = Field(
        json_schema_extra={"xml_type": "element"},
    )
    languageCode: CS | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "HumanLanguage",
            "binding_strength": "required",
        }
    )
    modeCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "LanguageAbilityMode",
            "binding_strength": "extensible",
        }
    )
    proficiencyLevelCode: CE | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "LanguageAbilityProficiency",
            "binding_strength": "extensible",
        }
    )
    preferenceInd: BL | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
