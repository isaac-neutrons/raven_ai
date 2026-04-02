from models.odm.datamodel import DataModel
from pydantic import Field
import datetime
from typing import Optional
from datetime import datetime, timezone
from typing import Literal
from pydantic import Field, AliasChoices

class Measurement(DataModel): 
    proposal_number:str
    facility:Literal["SNS", "HFIR", "LCLS"]
    instrument: Literal["REF_L"]
    laboratory:Literal["ORNL", "SLAC"]
    probe:Literal["neutrons", "xray", "other"]
    technique: Literal["Reflectivity"] 
    technique_description: str # prepend the technique value above of the raw data
    is_simulated:bool =False
    run_title:str
    run_number:Optional[str]
    run_start: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_file_path:str

    
class Reflectivity(Measurement):    
    q_1_angstrom:list[float] = Field(default_factory=list)
    r:list[float] = Field(default_factory=list)
    d_r: list[float] = Field(default_factory=list)
    d_q: list[float] = Field(default_factory=list)
    measurement_geometry:str   #float
    reduction_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reduction_version: str


class EIS(Measurement):
    frequency:float
    duration:float
    real_z: float
    imaginery_z: float
    phase:float
    potential:str


