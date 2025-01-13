from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FeatureRequest(BaseModel):
    Title: str
    Description: str
    Category: str
    Vote: int
    time_stamp: datetime = None
    class Config:
        orm_mode = True


class Bugs(BaseModel):
    Title: str
    Description: str
    Category: str
    Vote: int
    time_stamp: datetime = None

    class Config:
        orm_mode = True

class Automations(BaseModel):
    Title: str
    Description: str
    Vote: int
    time_stamp: datetime = None

    class Config:
        orm_mode = True

class Integrations(BaseModel):
    Title: str
    Description: str
    Vote: int
    time_stamp: datetime = None

    class Config:
        orm_mode = True

class Languages(BaseModel):
    Title: str
    Description: str
    Vote: int
    time_stamp: datetime = None

    class Config:
        orm_mode = True

class PublicAPI(BaseModel):
    Title: str
    Description: str
    Category: str
    Vote: int
    time_stamp: datetime = None