from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer, model_validator


# -----------------------------
# ENUMS

class PriSecEnum(Enum):
    pri = "1"
    sec = "2"
    EMPTY = "-1"
# -----------------------------
PRI_SEC_FIELDS = [
    "prematurity_nar", "lbw_nar", "asphyxia_nar", "rds_nar",
    "sepsis_nar", "jaundice_diag_nar", "meconium_aspiration_nar", "meningitis_nar",
    "congenital_anomaly_nar", "multiple_gestation_nar", "other_diagnosis_nar",
]

# -----------------------------
# MODEL

class AdmissionDiagnosis(BaseModel):
    prematurity_nar: Optional[Union[PriSecEnum, int]] = None
    lbw_nar: Optional[Union[PriSecEnum, int]] = None
    asphyxia_nar: Optional[Union[PriSecEnum, int]] = None
    rds_nar: Optional[Union[PriSecEnum, int]] = None
    sepsis_nar: Optional[Union[PriSecEnum, int]] = None
    jaundice_diag_nar: Optional[Union[PriSecEnum, int]] = None
    meconium_aspiration_nar: Optional[Union[PriSecEnum, int]] = None
    meningitis_nar: Optional[Union[PriSecEnum, int]] = None
    congenital_anomaly_nar: Optional[Union[PriSecEnum, int]] = None
    multiple_gestation_nar: Optional[Union[PriSecEnum, int]] = None
    other_diagnosis_nar: Optional[Union[PriSecEnum, int]] = None

    # -----------------------------
    # Normalizer
    @staticmethod
    def _normalize_enum(v, enum_cls):
        if v in (None, "", -1, "-1", "EMPTY"):
            return enum_cls.EMPTY
        if isinstance(v, enum_cls):
            return v
        try:
            return enum_cls(v)
        except Exception:
            return enum_cls.EMPTY

    # validator for all the rest
    @model_validator(mode="before")
    def normalize_all_enums(cls, values):
        for field in PRI_SEC_FIELDS:
            values[field] = cls._normalize_enum(values.get(field), PriSecEnum)
        return values


    # -----------------------------
    # Serializer
    @staticmethod
    def _serialize_enum(v):
        return -1 if isinstance(v, Enum) and v.value == "-1" else v.value if isinstance(v, Enum) else v

    @field_serializer(*PRI_SEC_FIELDS)
    def serialize_pri(self, v):
        return self._serialize_enum(v)