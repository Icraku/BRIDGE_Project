from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer


# -----------------------------
# ENUMS

class SexNar(Enum):
    F = "F"
    M = "M"
    I = "I"
    EMPTY = "-1"

class AgeUnits(Enum):
    days = "In days"
    hours = "In hours"
    EMPTY = "-1"

    def serialize_for_redcap(self):
        if self == AgeUnits.days:
            return "days"
        elif self == AgeUnits.hours:
            return "hours"
        elif self == AgeUnits.EMPTY:
            return -1

class GestationType(Enum):
    US = "U / S"
    LMP = "LMP"
    EMPTY = "-1"

class BabyFrom(Enum):
    Theatre = "Theatre"
    Labour = "Labour"
    Postnatal = "Postnatal"
    Paeds = "Paeds"
    Referral = "Referral"
    Home = "Home"
    EMPTY = "-1"


# -----------------------------
# MODEL

class InfantDetails(BaseModel):
    infant_ipno_nar: str
    doa_date_nar: str
    time_seen_nar: str
    sex_nar: Optional[Union[SexNar, int]] = None
    dob_date_nar: str
    time_birth_nar: str
    gestation_nar: str
    gest_type_nar: Optional[Union[GestationType, int]] = None
    age_units_itf: Optional[Union[AgeUnits, int]] = None
    infant_age_itf: str
    apgar_1m_itf: str
    apgar_5m_itf: str
    apgar_10m_itf: str
    baby_from_itf: Optional[Union[BabyFrom, int]] = None

    # -----------------------------
    # Serializer helper

    @staticmethod
    def _serialize_enum(v):
        if isinstance(v, AgeUnits):
            return v.serialize_for_redcap()
        if isinstance(v, Enum):
            return -1 if v.value == "-1" else v.value
        return v

    @field_serializer("sex_nar","gest_type_nar", "age_units_itf", "baby_from_itf")
    def serialize_enum(self, v):
        return self._serialize_enum(v)

    # -----------------------------
    # Normalizers

    @classmethod
    def _normalize_enum(cls, v, enum_cls):
        if v in (None, "", -1, "-1", "EMPTY"):
            return enum_cls.EMPTY
        try:
            # Special case for AgeUnits
            if enum_cls == AgeUnits:
                if v.lower() in ("days", "hours"):
                    return AgeUnits[v.lower()]
            return enum_cls(v)
        except Exception:
            return v

    @field_validator("sex_nar", mode="before")
    def normalize_sexnar(cls, v):
        return cls._normalize_enum(v, SexNar)

    @field_validator("gest_type_nar", mode="before")
    def normalize_gesttype(cls, v):
        return cls._normalize_enum(v, SexNar)

    @field_validator("age_units_itf", mode="before")
    def normalize_ageunits(cls, v):
        return cls._normalize_enum(v, AgeUnits)

    @field_validator("baby_from_itf", mode="before")
    def normalize_babyfrom(cls, v):
        return cls._normalize_enum(v, BabyFrom)
