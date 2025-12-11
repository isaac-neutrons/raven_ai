from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional
from models.materialdata import MaterialData


class EnvironmentData(DataModel):
  #__collection_name__: str = "environment_data"

  description:str
  ambiant_medium:Optional[MaterialData]
  temperature:Optional[float]= Field(default_factory=list)
  pressure:Optional[float] = Field(default_factory=list) 
  relative_humidity:Optional[float] = Field(default_factory=list) 
 