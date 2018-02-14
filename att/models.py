from .database import Base
from sqlalchemy import Column, Integer, String, Date, Time


class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    date = Column(Date)
    time = Column(Time)

    def __init__(self, description=None, date=None, time=None):
        self.description = description
        self.date = date
        self.time = time

    def as_dict(self):
        return {'description': self.description, 'date': self.date, 'time': self.time}
