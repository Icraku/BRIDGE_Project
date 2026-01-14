from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, field_validator, field_serializer

# -----------------------------
# ENUMS

class SkinNar(Enum):
    Normal = "Normal"
    Bruising = "Bruising"
    Rash = "Rash"
    Pustules = "Pustules"
    Mottling = "Mottling"
    EMPTY = "-1"

class AppearanceNar(Enum):
    Well = "Well"
    Sick = "Sick"
    Dysmorphic = "Dysmorphic"
    EMPTY = "-1"

class JaundiceNar(Enum):
    None_ = "None"
    Mild = "+"
    Severe = "+++"
    EMPTY = "-1"

class PallorNar(Enum):
    None_ = "None"
    Mild = "+"
    Severe = "+++"
    EMPTY = "-1"

class CryNar(Enum):
    Normal = "Normal"
    Weak = "Weak/Absent"
    Hoarse = "Hoarse"
    EMPTY = "-1"

class XiphoidNar(Enum):
    None_ = "None"
    Mild = "Mild"
    Severe = "Severe"
    EMPTY = "-1"

class IntercostalNar(Enum):
    None_ = "None"
    Mild = "Mild"
    Severe = "Severe"
    EMPTY = "-1"

class BulgingFontanelleNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class IrritableNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class ToneNar(Enum):
    Normal = "Normal"
    Increased = "Increased"
    Decreased = "Decreased"
    EMPTY = "-1"

class UmbilicusNar(Enum):
    Clean = "Clean"
    Local = "Local Pus"
    Pus = "Pus + Red Skin"
    Others = "Others"
    EMPTY = "-1"

class BirthDefectsNar(Enum):
    Yes = "Yes"
    No = "No"
    EMPTY = "-1"

class BirthDefectLimbNar(Enum):
    Yes = "Selected"
    EMPTY = "-1"

class SelectedEnum(Enum):
    Selected = "Selected"
    EMPTY = "-1"

# -----------------------------
# ENUM GROUPINGS

YES_NO_FIELDS = ["bulging_fontanelle_nar", "irritable_nar"]

OTHER_ENUM_FIELDS = [
    "skin_nar", "appearance_nar", "jaundice_nar", "pallor_nar",
    "cry_nar", "xiphoid_nar", "intercostal_nar", "tone_nar",
    "umbilicus_nar", "birth_defects_nar"
]

SELECTED_ENUM_FIELDS = [
    "birth_defect_gi_nar", "birth_defect_tube_nar", "birth_defect_hydro_nar",
    "birth_defect_spina_nar", "birth_defect_palate_nar", "birth_defect_limb_nar",
    "birth_defect_micro_nar", "birth_defect_birth_nar"
]

# -----------------------------
# HELPERS — MotherDetails Style

def normalize_enum(v, enum_cls):
    if v in (None, "", -1, "-1", "EMPTY"):
        return enum_cls.EMPTY
    if isinstance(v, enum_cls):
        return v
    try:
        return enum_cls(v)
    except Exception:
        return enum_cls.EMPTY

def serialize_enum(v):
    if isinstance(v, Enum):
        return -1 if v.value == "-1" else v.value
    return v

# -----------------------------
# NESTED MODEL

class SpecificBirthDefects(BaseModel):
    birth_defect_gi_nar: Optional[SelectedEnum] = None
    birth_defect_tube_nar: Optional[SelectedEnum] = None
    birth_defect_hydro_nar: Optional[SelectedEnum] = None
    birth_defect_spina_nar: Optional[SelectedEnum] = None
    birth_defect_palate_nar: Optional[SelectedEnum] = None
    birth_defect_limb_nar: Optional[BirthDefectLimbNar] = None
    birth_defect_micro_nar: Optional[SelectedEnum] = None
    birth_defect_birth_nar: Optional[SelectedEnum] = None

    # Validators
    @field_validator(*SELECTED_ENUM_FIELDS, mode="before")
    def normalize_selected(cls, v, field):
        enum_cls = BirthDefectLimbNar if field.field_name == "birth_defect_limb_nar" else SelectedEnum
        return normalize_enum(v, enum_cls)

    # Serializers
    @field_serializer(*SELECTED_ENUM_FIELDS)
    def serialize_selected(self, v):
        return serialize_enum(v)

# -----------------------------
# MAIN MODEL

class NewbornAdmission(BaseModel):
    temp_nar: str
    resp_rate_nar: str
    pulse_rate_nar: str
    oximetry_nar: str
    birth_weight_nar: str
    weight_now_nar: str
    head_circ_nar: str
    length_nar: str
    blood_pressure_nar: str

    skin_nar: Optional[Union[SkinNar, int, str]] = None
    appearance_nar: Optional[Union[AppearanceNar, int, str]] = None
    jaundice_nar: Optional[Union[JaundiceNar, int, str]] = None
    pallor_nar: Optional[Union[PallorNar, int, str]] = None
    cry_nar: Optional[Union[CryNar, int, str]] = None
    xiphoid_nar: Optional[Union[XiphoidNar, int, str]] = None
    intercostal_nar: Optional[Union[IntercostalNar, int, str]] = None

    cap_refill_nar: str

    bulging_fontanelle_nar: Optional[Union[BulgingFontanelleNar, int, str]] = None
    irritable_nar: Optional[Union[IrritableNar, int, str]] = None

    tone_nar: Optional[Union[ToneNar, int, str]] = None
    umbilicus_nar: Optional[Union[UmbilicusNar, int, str]] = None
    birth_defects_nar: Optional[Union[BirthDefectsNar, int, str]] = None

    specific_defects: Optional[SpecificBirthDefects] = None

    # -----------------------------
    # Field Validators (using grouped lists)

    # YES/NO fields
    @field_validator(*YES_NO_FIELDS, mode="before")
    def normalize_yes_no(cls, v, field):
        enum_cls = BulgingFontanelleNar if field.field_name == "bulging_fontanelle_nar" else IrritableNar
        return normalize_enum(v, enum_cls)

    # OTHER ENUM fields
    @field_validator(*OTHER_ENUM_FIELDS, mode="before")
    def normalize_other_fields(cls, v, field):
        mapping = {
            "skin_nar": SkinNar,
            "appearance_nar": AppearanceNar,
            "jaundice_nar": JaundiceNar,
            "pallor_nar": PallorNar,
            "cry_nar": CryNar,
            "xiphoid_nar": XiphoidNar,
            "intercostal_nar": IntercostalNar,
            "tone_nar": ToneNar,
            "umbilicus_nar": UmbilicusNar,
            "birth_defects_nar": BirthDefectsNar
        }
        enum_cls = mapping[field.field_name]
        return normalize_enum(v, enum_cls)

    # -----------------------------
    # Serializers

    @field_serializer(*YES_NO_FIELDS)
    def serialize_yes_no(self, v):
        return serialize_enum(v)

    @field_serializer(*OTHER_ENUM_FIELDS)
    def serialize_other(self, v):
        return serialize_enum(v)
