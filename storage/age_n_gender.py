from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Age_n_gender(Base):
    """Age and Gender of the user"""


    __tablename__ = "age_n_gender"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    user_name = Column(String(250), nullable=False)
    user_age = Column(Integer, nullable=False)
    user_gender = Column(String(1), nullable=False)
    timestamp = Column(String(100), nullable=False)
    trace_id = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, user_id, user_name, user_age, user_gender, timestamp, trace_id):
        """Initialize age and gender reading"""
        self.user_id = user_id
        self.user_name = user_name
        self.user_age = user_age
        self.user_gender = user_gender
        self.timestamp = timestamp
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()


    def to_dict(self):
        """Returns the dictionary representaion of the age and gender reading"""

        dict={}
        dict['user_id'] = self.user_id
        dict['user_name'] = self.user_name
        dict['user_age'] = self.user_age
        dict['user_gender'] = self.user_gender
        dict['timestamp'] = self.timestamp
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created


        return dict