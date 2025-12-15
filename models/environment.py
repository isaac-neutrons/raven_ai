from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional
from models.material import Material

class Environment(DataModel):

  description:str
  ambiant_medium:Optional[Material]
  temperature:Optional[float]= Field(default_factory=list)
  pressure:Optional[float] = Field(default_factory=list) 
  relative_humidity:Optional[float] = Field(default_factory=list) 
  measurements_ids: Optional[list[str]] = Field(default_factory=list) # point to Measurements
