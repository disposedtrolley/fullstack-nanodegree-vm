from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET request)
@app.route("/restaurants/<int:restaurant_id>/menu/JSON")
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,
                                             id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route("/")
@app.route("/restaurants/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template("menu.html", restaurant=restaurant, items=items)


@app.route("/restaurant/<int:restaurant_id>/new/", methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    # Task 1: Create route for newMenuItem function here
    if request.method == "POST":
        newItem = MenuItem(name=request.form["name"],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant_id=restaurant_id)


@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/edit/",
           methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    # Task 2: Create route for editMenuItem function here
    itemToEdit = session.query(MenuItem). \
                     filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == "POST":
        itemToEdit.name = request.form["name"]
        session.add(itemToEdit)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for("restaurantMenu",
                                restaurant_id=itemToEdit.restaurant_id))
    else:
        return render_template("editmenuitem.html", item=itemToEdit)


@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/delete/",
           methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    # Task 3: Create a route for deleteMenuItem function here
    itemToDelete = session.query(MenuItem). \
                     filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for("restaurantMenu",
                                restaurant_id=itemToDelete.restaurant_id))
    else:
        return render_template("deletemenuitem.html",
                               restaurant_id=restaurant_id,
                               item=itemToDelete)

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
