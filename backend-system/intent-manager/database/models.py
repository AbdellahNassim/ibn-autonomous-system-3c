from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import datetime
import enum
class IntentStatus(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    DEPLOYED = "DEPLOYED"



Base = declarative_base()
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
