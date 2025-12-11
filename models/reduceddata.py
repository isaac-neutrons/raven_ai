from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
import datetime
from typing import Optional, List

class Reflectivity(BaseModel):    
    q_1_angstrom:float
    r: float
    dR: float
    dQ:float
    measurement_geometry:float


class EIS(BaseModel):
    frequency:float
    z: float


class ReducedData(DataModel):
    _collection_name: str = "experiment"

    run_title:str
    run_number:str
    run_start: datetime.datetime.now(datetime.UTC)
    reduction_time: datetime.datetime.now(datetime.UTC)
    reflectivity_data: Optional[List[Reflectivity]] = Field(default_factory=list)
    eis: Optional[List[EIS]] = Field(default_factory=list)    