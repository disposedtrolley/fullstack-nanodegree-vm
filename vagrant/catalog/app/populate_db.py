from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
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

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

for category in categories:
    new_cat = Category(name=category)
    session.add(new_cat)
    session.commit()

for item in items:
    category = session.query(Category).filter_by(name=item.get("category")).one()
    new_item = Item(name=item.get("name"),
                    category_name=category.name,
                    description=item.get("description"),
                    user_id=1)
    session.add(new_item)
    session.commit()

print "added items!"
