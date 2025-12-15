from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional, List
from sample import Sample

class Experiment(DataModel):
    ipts:str    
    sample: Sample
