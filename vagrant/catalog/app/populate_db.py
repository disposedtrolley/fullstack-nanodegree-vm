from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


categories = ["Soccer",
              "Basketball",
              "Baseball",
              "Frisbee",
              "Snowboarding",
              "Rock Climbing",
              "Foosball",
              "Skating",
              "Hockey"]

items = [{"name": "Stick", "category": "Hockey", "description": "This is the description."},
         {"name": "Goggles", "category": "Snowboarding", "description": "This is the description."},
         {"name": "Snowboard", "category": "Snowboarding", "description": "This is the description."},
         {"name": "Two shinguards", "category": "Soccer", "description": "This is the description."},
         {"name": "Shinguards", "category": "Soccer", "description": "This is the description."},
         {"name": "Frisbee", "category": "Frisbee", "description": "This is the description."},
         {"name": "Bat", "category": "Baseball", "description": "This is the description."},
         {"name": "Jersey", "category": "Soccer", "description": "This is the description."},
         {"name": "Soccer Cleats", "category": "Soccer", "description": "This is the description."}]


for category in categories:
    new_cat = Category(name=category)
    session.add(new_cat)
    session.commit()


for item in items:
    category = session.query(Category).filter_by(name=item.get("category")).one()
    new_item = Item(name=item.get("name"),
                    category_name=category.name,
                    description=item.get("description"))
    session.add(new_item)
    session.commit()

print "added menu items!"
