from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class HealtStatusModel(BaseModel):
    quantityOfEngOilIcon: Optional[Any] = None
    vin: str
    warning: Optional[Any] = None
    wnglastUpdTime: datetime
