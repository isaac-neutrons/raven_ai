from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional
from models.material import Material
from datetime import datetime, timezone

class Environment(DataModel):

  description:str
  ambiant_medium:Optional[Material]
  temperature:Optional[float]= None
  pressure:Optional[float]= None
  relative_humidity:Optional[float] = None
  measurements_ids: Optional[list[str]] = Field(default_factory=list) # point to Measurements
  timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

  @classmethod
  def get_foreign_key_fields(cls):
    return ["measurements_ids"]