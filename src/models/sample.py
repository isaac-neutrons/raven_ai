from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
from typing import Optional
from models.material import Material



class Layer(BaseModel):
  material: Material
  thickness: float
  roughness: Optional[float] = None
  sld: Optional[float] = None

class Sample(DataModel):
  description:str
  environment_ids:list[str]=Field(min_length=1) #Environment
  substrate:Layer
  main_composition:str #periodic table composition validated through: periodictable
  geometry: Optional[str] = None # from substrate not required
  layers:list[Layer] = Field(min_length=1,max_length=5) #all the layer including the main one!
  publication_ids:list[str] = Field(default_factory=list) #Publication

  @classmethod
  def get_foreign_key_fields(cls):
    return ["environment_ids","publication_ids"]