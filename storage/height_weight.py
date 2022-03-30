from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Height_n_weight(Base):
    """Height and Weight of the user"""


    __tablename__ = "height_n_weight"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    user_name = Column(String(250), nullable=False)
    user_height = Column(Integer, nullable=False)
    user_weight = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    trace_id = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, user_id, user_name, user_height, user_weight, timestamp, trace_id):
        """Initialize age and gender reading"""
        self.user_id = user_id
        self.user_name = user_name
        self.user_height = user_height
        self.user_weight = user_weight
        self.timestamp = timestamp
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        """Returns the dictionary representaion of the age and gender reading"""

        dict={}
        dict['user_id'] = self.user_id
        dict['user_name'] = self.user_name
        dict['user_height'] = self.user_height
        dict['user_weight'] = self.user_weight
        dict['timestamp'] = self.timestamp
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created


        return dict