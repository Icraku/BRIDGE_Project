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


"""
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
"""

class GestationType(Enum):
    US = "U / S"
    LMP = "LMP"
    EMPTY = "-1"

class BVM(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class DeliveryNar(Enum):
    SVD = "SVD"
    CS = "CS"
    Breech = "Breech"
    Forceps = "Forceps"
    Vacuum = "Vacuum"
    EMPTY = "-1"

class CsTypeNar(Enum):
    Emergency = "Emergency"
    Elective = "Elective"
    EMPTY = "-1"

class MutipleDeliveryNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class BornOutsideNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class BornWhereNar(Enum):
    Home = "Home/Roadside"
    Other = "Other facility"
    EMPTY = "-1"

"""
class BabyFrom(Enum):
    Theatre = "Theatre"
    Labour = "Labour"
    Postnatal = "Postnatal"
    Paeds = "Paeds"
    Referral = "Referral"
    Home = "Home"
    EMPTY = "-1"
"""
"""    
    age_units_itf: Optional[Union[AgeUnits, int]] = None
    age_nar: str # THIS VALUE WOULD HAVE BEEN FOR HOURS OR DAYS FROM AGE_UNITS
    baby_from_itf: Optional[Union[BabyFrom, int]] = None
"""


# -----------------------------
# MODEL

class InfantDetails(BaseModel):
    infant_ipno_nar: str
    doa_date_nar: str
    time_seen_nar: str
    sex_nar: Optional[SexNar] = None
    dob_date_nar: str
    time_birth_nar: str
    gestation_nar: str
    gest_type_nar: Optional[GestationType] = None
    age_days_nar: str
    rom_nar: Optional[int] = None
    delivery_nar: Optional[DeliveryNar] = None
    cs_type_nar: Optional[CsTypeNar] = None
    bvm_nar: Optional[BVM] = None
    apgar_1m_itf: str
    apgar_5m_itf: str
    apgar_10m_itf: str
    mutiple_delivery_nar: Optional[MutipleDeliveryNar] = None
    multiple_deliver_count_nar: str
    born_outside_nar: Optional[BornOutsideNar] = None
    born_where_nar: Optional[BornWhereNar] = None



    # -----------------------------
    # Serializer helper

    @staticmethod
    def _serialize_enum(v):
        if isinstance(v, Enum):
            return -1 if v.value == "-1" else v.value
        return v


    @field_serializer("sex_nar", "gest_type_nar", "delivery_nar", "cs_type_nar", "bvm_nar", "mutiple_delivery_nar", "born_outside_nar", "born_where_nar")
    def serialize_enum(self, v):
        return self._serialize_enum(v)

    # -----------------------------
    # Normalizers
    @staticmethod
    def _normalize_enum(v, enum_cls):
        if v in (None, "", -1, "-1"):
            return enum_cls.EMPTY
        if isinstance(v, enum_cls):
            return v
        try:
            return enum_cls(v)
        except Exception:
            return enum_cls.EMPTY


    @field_validator("sex_nar", mode="before")
    def normalize_sexnar(cls, v):
        return cls._normalize_enum(v, SexNar)

    @field_validator("gest_type_nar", mode="before")
    def normalize_gesttype(cls, v):
        return cls._normalize_enum(v, SexNar)

    @field_validator("delivery_nar", mode="before")
    def normalize_deliverynar(cls, v):
        return cls._normalize_enum(v, DeliveryNar)

    @field_validator("cs_type_nar", mode="before")
    def normalize_cs_type_nar(cls, v):
        return cls._normalize_enum(v, CsTypeNar)

    @field_validator("bvm_nar", mode="before")
    def normalize_bvm_nar(cls, v):
        return cls._normalize_enum(v, BVM)

    @field_validator("mutiple_delivery_nar", mode="before")
    def normalize_mutiple_delivery_nar(cls, v):
        return cls._normalize_enum(v, MutipleDeliveryNar)

    @field_validator("born_outside_nar", mode="before")
    def normalize_born_outside_nar(cls, v):
        return cls._normalize_enum(v, BornOutsideNar)

    @field_validator("born_where_nar", mode="before")
    def normalize_born_where_nar(cls, v):
        return cls._normalize_enum(v, BornWhereNar)
