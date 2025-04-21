"""Logical Model: InfrastructureRoot (Base Type for all CDA Classes) ( Abstract ).

https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InfrastructureRoot.html
"""

from pydantic import Field

from CDA.logical_models.ANY import ANY
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II


class InfrastructureRoot(ANY):
    """Logical Model: InfrastructureRoot (Base Type for all CDA Classes) ( Abstract ).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-InfrastructureRoot.html
    """

    realmCode: list[CS] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    typeId: II | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    templateId: list[II] | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
