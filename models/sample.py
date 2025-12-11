from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
from typing import Optional
from environmentdata import EnvironmentData


class MaterialData(BaseModel):
  Composition: str
  Mass: Optional[float] = None

class SubstrateData(BaseModel):
  material: MaterialData
  dimensions: Optional[dict] = Field(default_factory=dict)


class LayerData(BaseModel):
  material: MaterialData
  order: int
  thickness: float


class Sample(DataModel):
  _collection_name: str = "sample"

  description:str
  environment: EnvironmentData
  substrate:MaterialData
  main_layer: Optional[LayerData]
  layers:list = Field(default_factory=dict) #min=1, max=5