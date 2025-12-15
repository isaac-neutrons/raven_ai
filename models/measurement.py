from models.odm.datamodel import DataModel
from pydantic import BaseModel, Field
import datetime
from typing import Optional, List



class Measurement(DataModel): 
    run_title:str
    run_number:Optional[str]
    run_start: datetime.datetime.now(datetime.UTC)
    raw_file_path:str

class Reflectivity(Measurement):    
    q_1_angstrom:float
    r: float
    dR: float
    dQ:float
    measurement_geometry:float
    reduction_time: datetime.datetime.now(datetime.UTC)


class EIS(Measurement):
    frequency:float
    z: float
