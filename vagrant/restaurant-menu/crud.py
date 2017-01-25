from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Tells our program which database engine we want to communicate with.
engine = create_engine('sqlite:///restaurantmenu.db')

# Make connection between class definitions and tables in the database.
Base.metadata.bind = engine

# Establish link between our code executions and the engine we just created.
# CRUD operations in SQLAlchemy are performed within a session.
# Sessions allow us to write down all the commands we want to execute but
# won't send them to the database until we commit
DBSession = sessionmaker(bind=engine)

session = DBSession()

# CREATE
# Add a restaurant.
myFirstRestaurant = Restaurant(name="Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

# Add a menu item.
cheesepizza = MenuItem(name="Cheese Pizza",
                       description="Made with all natural ingredients and \
                                    fresh mozzarella",
                       course="Entree",
                       price="$8.99",
                       restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()


# UPDATE
# 1. Find entry through query
# 2. Update values in the Python object
# 3. Add object to the session
# 4. Commit

# Update price of all veggie burgers to $2.99
veggie_burgers = session.query(MenuItem).filter_by(name="Veggie Burger")
for vb in veggie_burgers:
    if vb.price != "$2.99":
        vb.price = "$2.99"
        session.add(vb)
        session.commit()

# DELETE
# 1. Find entry through query
# 2. session.delete(object)
# 3. Commit
spinach_ice_cream = session.query(MenuItem).filter_by(name="Spinach Ice Cream")
session.delete(spinach_ice_cream)
session.commit()
