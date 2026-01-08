from models.odm.datamodel import DataModel
from pydantic import Field
import datetime
from typing import Optional



class Measurement(DataModel): 
    proposal_number:str
    facility:str #enum : SNS, HFIR , LCLS
    lab:str #enum: SLAC 
    probe:str #enum only: neutrons, xray or other
    technique: str #enum: 
    technique_description: str # prepend the technique value above of the raw data
    is_simulated:bool =False
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
    duration:float
    real_z: float
    imaginery_z: float
    phase:float
    potential:str