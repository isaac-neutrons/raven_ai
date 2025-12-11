from models.odm.datamodel import DataModel
from pydantic import Field
from typing import Optional, List
from sample import Sample

class Experiment(DataModel):
    _collection_name: str = "experiment"
    ipts:str    
    sample: Sample
    reduced_data_ids:Optional [List[str]] = Field(
        default_factory=list,
        description="List of ReducedData document IDs (foreign key references)",
        foreign_key="ReducedData")
    raw_data_folder_path:str 
