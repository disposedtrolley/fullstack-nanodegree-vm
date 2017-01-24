import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# declarative_base ets our code know that our classes are SQLAlchemy classes
# which correspond to tables in our database.
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

    restaurant = relationship(Restaurant)


# Points to the database we're using.
engine = create_engine('sqlite:///restaurantmenu.db')

# Adds the classes we've created as database tables.
Base.metadata.create_all(engine)
