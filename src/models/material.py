from pydantic import BaseModel
from typing import Optional

class Material(BaseModel):
  name: str
  mass: Optional[float] = None
  density: Optional[float] = None
  sld: Optional[float] = None
  isld: Optional[float] = None

