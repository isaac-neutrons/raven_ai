from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
from typing import Optional
from models.material import Material



class Layer(BaseModel):
  material: Material
  thickness: float


# class Substrate(Layer):
#   #have a default value for thickeness
#   pass

class Sample(DataModel):
  description:str
  environment_ids:list[str] #Environment
  substrate:Layer
  main_composition:str #periodic table composition validated through: periodictable
  geometry: Optional[str] = None # from substrate not required
  layers:list[Layer] = Field(default_factory=list) #min=1, max=5 , all the layer including the main one!
  publication_ids:list[str] = Field(default_factory=list) #Publication