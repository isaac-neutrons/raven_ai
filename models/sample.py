from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
from typing import Optional
from models.material import Material


class Substrate(BaseModel):
  material: Material
  geometry: Optional[str] = None
  thickness: Optional[float]


class Layer(BaseModel):
  material: Material
  thickness: float


class Sample(DataModel):
  description:str
  environment_ids:list[str] #Environment
  substrate:Substrate
  main_layer_index:int #order index of the layers list
  layers:list[Layer] = Field(default_factory=list) #min=1, max=5