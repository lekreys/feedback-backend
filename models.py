from sqlalchemy import Column, String, Integer, TIMESTAMP , ARRAY
from database import Base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB



class FeatureRequest(Base):
    __tablename__ = "Feature Request"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Category = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP)
    image_url = Column(JSONB, nullable=True)  


class Bugs(Base):
    __tablename__ = "Bugs"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Category = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP)
    image_url = Column(JSONB, nullable=True)  


class Automations(Base):
    __tablename__ = "Automations"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP)
    image_url = Column(JSONB, nullable=True)  

class Integrations(Base):
    __tablename__ = "Integrations"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP)
    image_url = Column(JSONB, nullable=True)  

class Languages(Base):
    __tablename__ = "Languages"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP)
    image_url = Column(JSONB, nullable=True)  


class PublicAPI(Base):
    __tablename__ = "Public API"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String)   
    Description = Column(String)
    Category = Column(String)
    Vote = Column(Integer)
    time_stamp = Column(TIMESTAMP) 
    image_url = Column(JSONB, nullable=True)  
