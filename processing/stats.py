from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Stats(Base):
    """ Processing Statistics """
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    num_a_g_readings = Column(Integer, nullable=False)
    max_a_readings = Column(Integer, nullable=True)
    num_h_w_readings = Column(Integer, nullable=False)
    max_h_readings = Column(Integer, nullable=True)
    max_w_readings = Column(Integer, nullable=True)
    last_updateds = Column(DateTime, nullable=False)
    
def __init__(self, num_a_g_readings, max_a_readings,
    num_h_w_readings, max_h_readings, max_w_readings,
    last_updateds):
    """ Initializes a processing statistics objet """
    self.num_a_g_readings = num_a_g_readings
    self.max_a_readings = max_a_readings
    self.num_h_w_readings = num_h_w_readings
    self.max_h_readings = max_h_readings
    self.max_w_readings = max_w_readings
    self.last_updateds = last_updateds




def to_dict(self):
    """ Dictionary Representation of a statistics """
    dict = {}
    dict['num_a_g_readings'] = self.num_a_g_readings
    dict['max_a_readings'] = self.max_a_readings
    dict['num_h_w_readings'] = self.num_h_w_readings
    dict['max_h_readings'] = self.max_h_readings
    dict['max_w_readings'] = self.max_w_readings
    dict['last_updateds'] = self.last_updateds.strftime(f"%Y-%m-%dT%H:%M:%S")
    return dict