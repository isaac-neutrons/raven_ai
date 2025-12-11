from pydantic import BaseModel
from typing import Optional

class MaterialData(BaseModel):
  composition: str
  mass: Optional[float] = None

