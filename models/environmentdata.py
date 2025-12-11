from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional
from sample import MaterialData

class EnvironmentData(DataModel):
  _collection_name: str = "environment_data"

  description:str
  ambiant_medium:MaterialData
  temperature:Optional[float]= Field(default_factory=list)
  pressure:Optional[float] = Field(default_factory=list) 
  relative_humidity:Optional[float] = Field(default_factory=list) 
 