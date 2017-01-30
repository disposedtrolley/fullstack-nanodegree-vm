from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    description = Column(String(2000))
    category_name = Column(String(250), ForeignKey("category.name"))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    created_at = Column(DateTime, default=datetime.datetime.now())

    @property
    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "creator_id": self.user_id,
            "id": self.id,
            "category": self.category_name
        }


if __name__ == "__main__":
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.create_all(engine)
