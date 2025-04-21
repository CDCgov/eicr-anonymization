from typing import Literal

from pydantic import BaseModel, Field

from CDA.data_types.string_validators import cs
from CDA.logical_models.AD import AD
from CDA.logical_models.BL import BL
from CDA.logical_models.CD import CD
from CDA.logical_models.CE import CE
from CDA.logical_models.CV import CV
from CDA.logical_models.ED import ED
from CDA.logical_models.EIVL_TS import EIVL_TS
from CDA.logical_models.EN import EN
from CDA.logical_models.II import II
from CDA.logical_models.INT import INT
from CDA.logical_models.IVL_PQ import IVL_PQ
from CDA.logical_models.IVL_TS import IVL_TS
from CDA.logical_models.MO import MO
from CDA.logical_models.PIVL_TS import PIVL_TS
from CDA.logical_models.PQ import PQ
from CDA.logical_models.REAL import REAL
from CDA.logical_models.SC import SC
from CDA.logical_models.ST import ST
from CDA.logical_models.SXPR_TS import SXPR_TS
from CDA.logical_models.TEL import TEL
from CDA.logical_models.TS import TS


class Criterion(BaseModel):
    """Logical Model: Criterion (CDA Class).

    https://build.fhir.org/ig/HL7/CDA-core-2.0/StructureDefinition-Criterion.html
    """

    classCode: cs = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActClassObservation",
            "binding_strength": "required",
        }
    )
    moodCode: Literal["EVN.CRT"] = Field(
        json_schema_extra={
            "xml_type": "attribute",
            "binding": "ActMoodPredicate",
            "binding_strength": "required",
            "fixed_value": "EVN.CRT",
        }
    )
    templateId: list[II] | None = Field(json_schema_extra={"xml_type": "element"})
    code: CD | None = Field(
        json_schema_extra={
            "xml_type": "element",
            "binding": "v3 Code System ActCode",
            "binding_strength": "extensible",
        }
    )
    text: ED | None = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
    value: (
        BL
        | ED
        | ST
        | CD
        | CV
        | CE
        | SC
        | II
        | TEL
        | AD
        | EN
        | INT
        | REAL
        | PQ
        | MO
        | TS
        | IVL_PQ
        | IVL_TS
        | PIVL_TS
        | EIVL_TS
        | SXPR_TS
        | TS
        | None
    ) = Field(
        json_schema_extra={
            "xml_type": "element",
        }
    )
