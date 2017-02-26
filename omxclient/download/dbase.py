#This uses sqlalchemy as sqlite engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker

# Create the engine

DB_TYPE="mysql+pymysql"
USER = "jutil"
PASS = "gamma007"
HOST = "192.168.1.68"
DB = "omxclient"
engine = create_engine(DB_TYPE+'://'+USER+':'+PASS+'@'+HOST+'/'+DB)
#engine = create_engine('sqlite:///omxclient.db', echo=True)

Base = declarative_base()

class DownloadRequest(Base):
     __tablename__ = 'downloadRequest'

     id = Column(Integer, primary_key=True)
     service = Column(String(128))
     url = Column(String(512))

     def toSerializable(self):
         return {'id':self.id,'service':self.service,'url':self.url}

     def __repr__(self):
        return "<DownloadRequest(id='%s',service='%s', request='%s')>" % (
                             self.id, self.service, self.url)

#Create the database
Base.metadata.create_all(engine)
#Setup the a session engine
session_factory = sessionmaker(bind=engine)
