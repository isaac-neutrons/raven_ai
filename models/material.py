from pydantic import BaseModel
from typing import Optional

class Material(BaseModel):
  composition: str
  mass: Optional[float] = None

