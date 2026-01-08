from models.odm.datamodel import DataModel
from pydantic import Field


class Publication(DataModel):
    title: str
    url:str
    abstract:str
    notes:str
    keywords:list[str] = Field(default_factory=list)
