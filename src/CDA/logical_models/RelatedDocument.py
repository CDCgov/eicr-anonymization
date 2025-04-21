from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.CS import CS
from CDA.logical_models.II import II
from CDA.logical_models.ParentDocument import ParentDocument
from CDA.value_sets.NullFlavor import NullFlavor


class RelatedDocument(BaseModel):
    """Logical Model: RelatedDocument (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-RelatedDocument.html
    """

    nullFlavor: NullFlavor | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "NullFlavor",
            "binding_strength": "required",
        }
    )
    typeCode: cs | None = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "x_ActRelationshipDocument",
            "binding_strength": "required",
        }
    )
    realmCode: list[CS] | None = Field(json_schema_extra={"xml_type": "element"})
    typeId: II | None = Field(json_schema_extra={"xml_type": "element"})
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    parentDocument: ParentDocument = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
