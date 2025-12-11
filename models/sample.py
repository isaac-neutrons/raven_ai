from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
from typing import Optional
from models.environmentdata import EnvironmentData
from models.materialdata import MaterialData


class SubstrateData(BaseModel):
  material: MaterialData
  dimensions: Optional[dict] = Field(default_factory=dict) # TODO dict[?]


class LayerData(BaseModel):
  material: MaterialData
  thickness: float


class Sample(DataModel):
  _collection_name: str = "sample"

  description:str
  environmentId:str #EnvironmentData
  substrate:SubstrateData
  main_layer: Optional[LayerData]
  layers:list[LayerData] = Field(default_factory=dict) #min=1, max=5