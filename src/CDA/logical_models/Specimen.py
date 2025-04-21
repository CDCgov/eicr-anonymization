from typing import Literal

from pydantic import Field

from CDA.logical_models.InfrastructureRoot import InfrastructureRoot
from CDA.logical_models.SpecimenRole import SpecimenRole


class Specimen(InfrastructureRoot):
    """Logical Model: Specimen (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Specimen.html
    """

    typeCode: Literal["SPC"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ParticipationTargetDirect",
            "binding_strength": "required",
            "fixed_value": "SPC",
        }
    )
    specimenRole: SpecimenRole = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
