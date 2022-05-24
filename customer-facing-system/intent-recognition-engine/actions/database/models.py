from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    """
        User model
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # This property will allow us to simplifies the queries it won't be added to the schema
    intents = relationship("Intent", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return "<User(username='{}', password='{}')>"\
                .format(self.username, self.password)

class Intent(Base):
    """
        Intent model 
    """
    __tablename__ = 'intent'
    id = Column(String, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    service_id = Column(Integer, ForeignKey('service.id'))
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
    delivery_status = Column(String, nullable=False)

    ## Relationships
    # This will allow us to have intent.user() and get all the intents of a user
    user = relationship("User", back_populates="intents")
    # With the use of uselist we make the relation one to one
    service = relationship("Service", back_populates="intent", uselist=False)
    
    def __repr__(self):
        return "<Intent(id='{}', user_id='{}', service_id='{}', request_date='{}', delivery_status='{}')>"\
                .format(self.id, self.user_id, self.service_id, self.request_date, self.delivery_status)


class Service(Base):
    """
        Service Model 
    """
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    type_id = Column(Integer, ForeignKey("service_type.id"))

    # This allow to have a many to one relationship where each intent service has a type
    type = relationship('ServiceType', back_populates='services')
    # Each service is requested by an intent 
    intent = relationship("Intent", back_populates='service', cascade="all, delete-orphan")
    # This won't be added to the database schema it will just help us in queries !
    # In django it is generated automatically but in sql alchemy it needs to be defined
    video_service_params = relationship("VideoServiceParams", back_populates="service", uselist=False, cascade="all, delete-orphan")
    def __repr__(self):
        return "<Service(service_id='{}', type_id='{}')>"\
                .format(self.id, self.type_id)

class ServiceType(Base):
    """
        Service Type model 
    """
    __tablename__ = 'service_type'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)
    provider_url = Column(String, nullable=False)

    ## Relationships
    # This will make us have a one to many relationship 
    services = relationship("Service", back_populates="type", cascade="all, delete-orphan")
    def __repr__(self):
        return "<ServiceType(id='{}', name='{}', provider_name='{}', provider_url='{}')>"\
                .format(self.id, self.name, self.provider_name, self.provider_url)


class VideoServiceParams(Base):
    """
        Params of the Video Service Model
    """
    __tablename__ = 'video_service_params'
    service_id = Column(Integer, ForeignKey('service.id'), primary_key=True)
    latency_min = Column(Integer, nullable=False)
    resolution = Column(String, nullable=False)
    # same thing to get the relationship 
    service = relationship("Service", back_populates="video_service_params")
    
    def __repr__(self):
        return "<VideoServiceParams(service_id='{}', latency_min='{}', resolution='{}')>"\
                .format(self.service_id, self.latency_min, self.resolution)
