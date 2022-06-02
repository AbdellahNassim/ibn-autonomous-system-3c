from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

Base = declarative_base()

class IntentStatus(enum.Enum):
    """
        Enum class that represents the status of delivery of the intent 
    """
    IN_PROGRESS = "IN_PROGRESS"
    DEPLOYED = "DEPLOYED"


class IntentTracker(Base):
    """
        IntentTracker table 
    """
    __tablename__ = 'intent_tracker'
    id = Column(String, primary_key=True, unique=True)
    intent_rdf = Column(String, nullable=False)
    status = Column(Enum(IntentStatus), nullable=False)
    
    def __repr__(self):
        return "<IntentTracker(id='{}',intent_rdf='{}' status='{}')>"\
                .format(self.id, self.intent_rdf , self.status)

class ServicesCatalog(Base):
    """
        Services Catalog Table 
    """
    __tablename__ = 'services_catalog'
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    service_type = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    service_repository = Column(String, nullable=False)
    service_repository_url = Column(String, nullable=False)
    
    def __repr__(self):
        return "<ServicesCatalog(id='{}', service_type='{}', service_name='{}', service_repository='{}', service_repository_url='{}')>"\
                .format(self.id, self.service_type, self.service_name, self.service_repository, self.service_repository_url)