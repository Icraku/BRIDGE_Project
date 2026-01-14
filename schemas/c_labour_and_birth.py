from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator, field_serializer, model_validator


# -----------------------------
# ENUMS

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

class YesNoEnum(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

YES_NO_FIELDS = [
    "meconium_itf", "steroids_itf", "bvm_itf", "chest_compress_itf",
    "oxygen_itf", "cpap_itf", "vit_k_itf", "hep_b_itf",
    "teo_itf", "bcg_itf", "opv_itf", "chlorohexidine_itf"
]

# -----------------------------
# MODEL

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

    # Individual validators for delivery, CS, maternal
    @field_validator("delivery_itf", mode="before")
    def normalize_delivery(cls, v):
        return cls._normalize_enum(v, DeliveryItf)

    @field_validator("cs_type_itf", mode="before")
    def normalize_cs_type(cls, v):
        return cls._normalize_enum(v, CsTypeItf)

    @field_validator("maternal_status_itf", mode="before")
    def normalize_maternal(cls, v):
        return cls._normalize_enum(v, MaternalStatusItf)

    # -----------------------------
    # Model-level validator for all yes/no fields
    @model_validator(mode="before")
    def normalize_yes_no_fields(cls, values):
        for field_name in YES_NO_FIELDS:
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

    @field_serializer(*YES_NO_FIELDS)
    def serialize_yes_no(self, v):
        return self._serialize_enum(v)
