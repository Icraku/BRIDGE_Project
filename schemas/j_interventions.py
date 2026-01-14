from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer, model_validator

# -----------------------------
# ENUMS

class YesNoEnum(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

YES_NO_FIELDS = [
    "vit_k_nar", "caffeine_citrate_nar", "bcg_nar", "prophylaxis_pmtct_nar",
    "chlorohexidine_nar", "kmc_nar", "incubate_warm_nar",
    "phototherapy_nar", "nutrition_feeds_nar", "opv_nar",
    "iv_fluids_nar", "transfusion_nar", "surfactant_nar",
    "antibiotics_nar", "oxygen_nar", "cpap_nar",
]

# -----------------------------
# MODEL

class Interventions(BaseModel):
    vit_k_nar: Optional[Union[YesNoEnum, int]] = None
    caffeine_citrate_nar: Optional[Union[YesNoEnum, int]] = None
    bcg_nar: Optional[Union[YesNoEnum, int]] = None
    prophylaxis_pmtct_nar: Optional[Union[YesNoEnum, int]] = None
    chlorohexidine_nar: Optional[Union[YesNoEnum, int]] = None
    kmc_nar: Optional[Union[YesNoEnum, int]] = None
    incubate_warm_nar: Optional[Union[YesNoEnum, int]] = None
    phototherapy_nar: Optional[Union[YesNoEnum, int]] = None
    nutrition_feeds_nar: Optional[Union[YesNoEnum, int]] = None
    opv_nar: Optional[Union[YesNoEnum, int]] = None
    iv_fluids_nar: Optional[Union[YesNoEnum, int]] = None
    transfusion_nar: Optional[Union[YesNoEnum, int]] = None
    surfactant_nar: Optional[Union[YesNoEnum, int]] = None
    antibiotics_nar: Optional[Union[YesNoEnum, int]] = None
    oxygen_nar: Optional[Union[YesNoEnum, int]] = None
    cpap_nar: Optional[Union[YesNoEnum, int]] = None

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
        for field in YES_NO_FIELDS:
            values[field] = cls._normalize_enum(values.get(field), YesNoEnum)
        return values


    # -----------------------------
    # Serializer
    @staticmethod
    def _serialize_enum(v):
        return -1 if isinstance(v, Enum) and v.value == "-1" else v.value if isinstance(v, Enum) else v

    @field_serializer(*YES_NO_FIELDS)
    def serialize_pri(self, v):
        return self._serialize_enum(v)

