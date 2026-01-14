from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer, model_validator

# -----------------------------
# ENUMS

# --- Infant Details ---
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

# --- Mother Details ---
class BloodGroupNar(Enum):
    A = "A"
    B = "B"
    AB = "AB"
    O = "O"
    Unkn = "Unkn"
    EMPTY = "-1"

class PosNegUnknEnum(Enum):
    Pos = "Pos"
    Neg = "Neg"
    Unkn = "Unkn"
    EMPTY = "-1"

class YesNoEnum(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class YesNoUnknEnum(Enum):
    Yes = "Yes"
    No = "No"
    Unkn = "Unkn"
    EMPTY = "-1"

POS_NEG_UNKN_FIELDS = ["rhesus_nar", "vdrl_nar", "pmtct_nar", "hepb_nar"]
YES_NO_FIELDS = ["anti_d_nar", "anc_us_nar"]
YES_NO_UNKN_FIELDS = ["mum_arvs_nar", "hepb_ig_nar", "htn_pregnancy_nar",
                      "aph_nar", "diabetes_nar", "prolonged_stage_nar"]

# --- Labour & Birth ---
class DeliveryItf(Enum):
    SVD = "SVD"
    CS = "CS"
    Breech = "Breech"
    Forceps = "Forceps"
    Vacuum = "Vacuum"
    EMPTY = "-1"

class CsTypeItf(Enum):
    Emergency = "Emergency"
    Elective = "Elective"
    EMPTY = "-1"

class MaternalStatusItf(Enum):
    Well = "Well"
    Unwell = "Unwell"
    Deceased = "Deceased"
    EMPTY = "-1"

YES_NO_LABOUR_FIELDS = [
    "meconium_itf", "steroids_itf", "bvm_itf", "chest_compress_itf",
    "oxygen_itf", "cpap_itf", "vit_k_itf", "hep_b_itf",
    "teo_itf", "bcg_itf", "opv_itf", "chlorohexidine_itf"
]

# -----------------------------
# MODELS

# --- Infant Details ---
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
            if enum_cls == AgeUnits and isinstance(v, str):
                return AgeUnits[v.lower()]
            return enum_cls(v)
        except Exception:
            return v

    @field_validator("sex_nar", mode="before")
    def normalize_sexnar(cls, v):
        return cls._normalize_enum(v, SexNar)

    @field_validator("gest_type_nar", mode="before")
    def normalize_gesttype(cls, v):
        return cls._normalize_enum(v, GestationType)

    @field_validator("age_units_itf", mode="before")
    def normalize_ageunits(cls, v):
        return cls._normalize_enum(v, AgeUnits)

    @field_validator("baby_from_itf", mode="before")
    def normalize_babyfrom(cls, v):
        return cls._normalize_enum(v, BabyFrom)


# --- Mother Details ---
class MotherDetails(BaseModel):
    mum_ip_no_nar: str
    mum_age_years_nar: str
    parity_nar: str
    edd_date_nar: str

    blood_group_nar: Optional[Union[BloodGroupNar, int]] = None
    rhesus_nar: Optional[Union[PosNegUnknEnum, int]] = None
    anti_d_nar: Optional[Union[YesNoEnum, int]] = None
    anc_visits_nar: str
    anc_us_nar: Optional[Union[YesNoEnum, int]] = None
    anc_trimester_nar: str
    vdrl_nar: Optional[Union[PosNegUnknEnum, int]] = None
    pmtct_nar: Optional[Union[PosNegUnknEnum, int]] = None
    mum_arvs_nar: Optional[Union[YesNoUnknEnum, int]] = None
    hepb_nar: Optional[Union[PosNegUnknEnum, int]] = None
    hepb_ig_nar: Optional[Union[YesNoUnknEnum, int]] = None
    htn_pregnancy_nar: Optional[Union[YesNoUnknEnum, int]] = None
    aph_nar: Optional[Union[YesNoUnknEnum, int]] = None
    diabetes_nar: Optional[Union[YesNoUnknEnum, int]] = None
    prolonged_stage_nar: Optional[Union[YesNoUnknEnum, int]] = None

    # -----------------------------
    # Normalizers
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

    @field_validator("blood_group_nar", mode="before")
    def normalize_blood(cls, v):
        return cls._normalize_enum(v, BloodGroupNar)

    @model_validator(mode="before")
    def normalize_all_enums(cls, values):
        for field in YES_NO_FIELDS:
            values[field] = cls._normalize_enum(values.get(field), YesNoEnum)
        for field in POS_NEG_UNKN_FIELDS:
            values[field] = cls._normalize_enum(values.get(field), PosNegUnknEnum)
        for field in YES_NO_UNKN_FIELDS:
            values[field] = cls._normalize_enum(values.get(field), YesNoUnknEnum)
        return values

    # -----------------------------
    # Serializers
    @staticmethod
    def _serialize_enum(v):
        return -1 if isinstance(v, Enum) and v.value == "-1" else v.value if isinstance(v, Enum) else v

    @field_serializer("blood_group_nar")
    def serialize_blood(self, v):
        return self._serialize_enum(v)

    @field_serializer(*YES_NO_FIELDS)
    def serialize_yes_no(self, v):
        return self._serialize_enum(v)

    @field_serializer(*POS_NEG_UNKN_FIELDS)
    def serialize_pos_neg_unkn(self, v):
        return self._serialize_enum(v)

    @field_serializer(*YES_NO_UNKN_FIELDS)
    def serialize_yes_no_unkn(self, v):
        return self._serialize_enum(v)


# --- Labour & Birth ---
class LabourAndBirth(BaseModel):
    delivery_itf: Optional[DeliveryItf] = None
    cs_type_itf: Optional[CsTypeItf] = None
    meconium_itf: Optional[YesNoEnum] = None
    steroids_itf: Optional[YesNoEnum] = None
    no_doses_itf: str
    bvm_itf: Optional[YesNoEnum] = None
    chest_compress_itf: Optional[YesNoEnum] = None
    resuscitation_itf: str
    oxygen_itf: Optional[YesNoEnum] = None
    cpap_itf: Optional[YesNoEnum] = None
    vit_k_itf: Optional[YesNoEnum] = None
    hep_b_itf: Optional[YesNoEnum] = None
    teo_itf: Optional[YesNoEnum] = None
    bcg_itf: Optional[YesNoEnum] = None
    opv_itf: Optional[YesNoEnum] = None
    chlorohexidine_itf: Optional[YesNoEnum] = None
    maternal_status_itf: Optional[MaternalStatusItf] = None

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

    @field_validator("delivery_itf", mode="before")
    def normalize_delivery(cls, v):
        return cls._normalize_enum(v, DeliveryItf)

    @field_validator("cs_type_itf", mode="before")
    def normalize_cs_type(cls, v):
        return cls._normalize_enum(v, CsTypeItf)

    @field_validator("maternal_status_itf", mode="before")
    def normalize_maternal(cls, v):
        return cls._normalize_enum(v, MaternalStatusItf)

    @model_validator(mode="before")
    def normalize_yes_no_fields(cls, values):
        for field_name in YES_NO_LABOUR_FIELDS:
            values[field_name] = cls._normalize_enum(values.get(field_name), YesNoEnum)
        return values

    # -----------------------------
    # Serializers
    @staticmethod
    def _serialize_enum(v):
        return -1 if isinstance(v, Enum) and v.value == "-1" else v.value if isinstance(v, Enum) else v

    @field_serializer("delivery_itf")
    def serialize_delivery(self, v):
        return self._serialize_enum(v)

    @field_serializer("cs_type_itf")
    def serialize_cs_type(self, v):
        return self._serialize_enum(v)

    @field_serializer("maternal_status_itf")
    def serialize_maternal(self, v):
        return self._serialize_enum(v)

    @field_serializer(*YES_NO_LABOUR_FIELDS)
    def serialize_yes_no(self, v):
        return self._serialize_enum(v)
