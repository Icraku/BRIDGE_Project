from enum import Enum
from typing import Optional
from pydantic import BaseModel, model_validator, field_serializer

# -----------------------------
# ENUMS

class YesNoEnum(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

# -----------------------------
# MODEL

YES_NO_FIELDS = [
    "fever_nar", "diff_breath_nar", "inability_feed_nar",
    "convulsions_nar", "apnoea_nar", "floppy_nar",
    "vomits_nar", "passed_stool_nar", "passed_urine_nar"
]

class PresentingProblems(BaseModel):
    fever_nar: Optional[YesNoEnum] = None
    diff_breath_nar: Optional[YesNoEnum] = None
    inability_feed_nar: Optional[YesNoEnum] = None
    convulsions_nar: Optional[YesNoEnum] = None
    apnoea_nar: Optional[YesNoEnum] = None
    floppy_nar: Optional[YesNoEnum] = None
    vomits_nar: Optional[YesNoEnum] = None
    passed_stool_nar: Optional[YesNoEnum] = None
    passed_urine_nar: Optional[YesNoEnum] = None

    # -----------------------------
    # Normalization
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

    @field_serializer(*YES_NO_FIELDS)
    def serialize_yes_no(self, v):
        return self._serialize_enum(v)
