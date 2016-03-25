#This uses sqlalchemy as sqlite engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker

# Create the engine
engine = create_engine('sqlite:///omxclient.db', echo=True)

Base = declarative_base()

class DownloadRequest(Base):
     __tablename__ = 'downloadRequest'

     id = Column(Integer, primary_key=True)
     service = Column(String)
     url = Column(String)

     def toSerializable(self):
         return {'id':self.id,'service':self.service,'url':self.url}

     def __repr__(self):
        return "<DownloadRequest(id='%s',service='%s', request='%s')>" % (
                             self.id, self.service, self.url)

#Create the database
Base.metadata.create_all(engine)
#Setup the a session engine
session_factory = sessionmaker(bind=engine)
