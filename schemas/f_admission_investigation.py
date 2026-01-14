from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer, model_validator

# -----------------------------
# ENUMS
 # Yes, Yes | No, No | -1, Empty

class RandomBloodSugarNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class BilirubinNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class AdmissionInvestigation(BaseModel):
    rbs_nar: Optional[Union[RandomBloodSugarNar, int]] = None
    rbs_measure_nar: str
    bilirubin_nar: Optional[Union[BilirubinNar, int]] = None
    serum_measure_nar: str

    # -----------------------------
    # Serializer helper

    @staticmethod
    def _serialize_enum(v):
        if isinstance(v, Enum):
            return -1 if v.value == "-1" else v.value
        return v

    @field_serializer("rbs_nar", "bilirubin_nar")
    def serialize_enum(self, v):
        return self._serialize_enum(v)

    # -----------------------------
    # Normalizers

    @classmethod
    def _normalize_enum(cls, v, enum_cls):
        if v in (None, "", -1, "-1", "EMPTY"):
            return enum_cls.EMPTY
        return v

    @field_validator("rbs_nar", mode="before")
    def normalize_rbs(cls, v):
        return cls._normalize_enum(v, RandomBloodSugarNar)

    @field_validator("bilirubin_nar", mode="before")
    def normalize_bilirubin(cls, v):
        return cls._normalize_enum(v, BilirubinNar)

