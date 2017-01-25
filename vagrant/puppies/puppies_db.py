import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# declarative_base ets our code know that our classes are SQLAlchemy classes
# which correspond to tables in our database.
Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(String(80), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(20), nullable=False)
    zipCode = Column(String(5), nullable=False)
    website = Column(String(60))
    id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    dob = Column(Date)
    gender = Column(String(1), nullable=False)
    weight = Column(Float(), nullable=False)

    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


# Points to the database we're using.
engine = create_engine('sqlite:///puppies.db')

# Adds the classes we've created as database tables.
Base.metadata.create_all(engine)
