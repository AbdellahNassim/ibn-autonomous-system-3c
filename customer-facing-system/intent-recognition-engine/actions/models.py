from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    """
        User model 
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return "<User(username='{}', password='{}')>"\
                .format(self.username, self.password)

class IntentService(Base):
    __tablename__ = 'intent_services'
    service_id = Column(Integer, primary_key=True)
    service_type = Column(String)

    # This is used to declare a one to one relationship 
    params = relationship("VideoServiceParams", back_populates="intent_services", uselist=False)
    
    def __repr__(self):
        return "<IntentService(service_id='{}', type='{}')>"\
                .format(self.service_id, self.service_type)


class VideoServiceParams(Base):
    """
        Params of the Video Service Model
    """
    __tablename__ = 'video_service_params'
    service_id = Column(Integer, primary_key=True)
    latency_min = Column(Integer)
    resolution = Column(String)
    # same thing to get the relationship 
    intent_service = relationship("IntentService", back_populates="video_service_params")
    
    def __repr__(self):
        return "<VideoServiceParams(service_id='{}', latency_min='{}', resolution='{}')>"\
                .format(self.service_id, self.latency_min, self.resolution)


class Intents(Base):
    """
        Intent model 
    """
    __tablename__ = 'intents'
    intent_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    service = Column(Integer, ForeignKey('intent_services.service_id'))
    request_date = Column(Date)
    status = Column(String)
    # This will allow us to have user.intents() and get all the intents of a user
    users = relationship("Users", back_populates="intents")
    
    def __repr__(self):
        return "<Intent(intent_id='{}', user_id='{}', service='{}', request_date='{}', status='{}')>"\
                .format(self.intent_id, self.user_id, self.service, self.request_date, self.status)