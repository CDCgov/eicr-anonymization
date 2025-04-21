from typing import Literal

from pydantic import Field

from CDA.logical_models.EncompassingEncounter import EncompassingEncounter
from CDA.logical_models.InfrastructureRoot import InfrastructureRoot


class ComponentOf(InfrastructureRoot):
    """Logical Model: ComponentOf (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-ComponentOf.html
    """

    typeCode: Literal["COMP"] | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActRelationshipHasComponent",
            "binding_strength": "required",
        }
    )
    encompassingEncounter: EncompassingEncounter = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
