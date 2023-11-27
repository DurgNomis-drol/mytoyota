from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_validator

from mytoyota.utils.logs import censor_vin


class HealtStatusModel(BaseModel):
    quantityOfEngOilIcon: Optional[Any] = None
    vin: str
    warning: Optional[Any] = None
    wnglastUpdTime: datetime

    @field_validator("vin")
    def censor_original_vin(cls, v):
        v = censor_vin(v)
        return v
