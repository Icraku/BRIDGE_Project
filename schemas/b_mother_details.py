from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer, model_validator

# -----------------------------
# ENUMS

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

# -----------------------------
POS_NEG_UNKN_FIELDS = [
    "rhesus_nar", "vdrl_nar", "pmtct_nar", "hepb_nar"
]

YES_NO_FIELDS = [
    "anti_d_nar", "anc_us_nar"
]

YES_NO_UNKN_FIELDS = [
    "mum_arvs_nar", "hepb_ig_nar", "htn_pregnancy_nar",
    "aph_nar", "diabetes_nar", "prolonged_stage_nar"
]

# -----------------------------
# MODEL

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

    # Individual validators for non Yes/No fields
    @field_validator("blood_group_nar", mode="before")
    def normalize_blood(cls, v):
        return cls._normalize_enum(v, BloodGroupNar)


    # validator for all the rest
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
    # Serializer
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