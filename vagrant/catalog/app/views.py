from flask import render_template, url_for, flash, redirect, request
from app import app
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item, User


# Connect to Database and create database session
engine = create_engine('sqlite:///app/itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def index():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template("home_auth.html",
                           curr_category="Latest Items",
                           categories=categories,
                           items=items)


@app.route("/<category>")
def category(category):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_name=category).all()
    return render_template("category_list.html",
                           curr_category=category,
                           categories=categories,
                           items=items)


@app.route("/<category>/<item>")
def item(category, item):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(category_name=category,
                                         name=item).first()
    user = session.query(User).filter_by(id=item.user_id).one()
    return render_template("item_auth.html",
                           item=item,
                           categories=categories,
                           user=user)


@app.route("/newitem", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        item_category = request.form["item-category"]
        item_name = request.form["item-name"]
        item_description = request.form["item-description"]
        if item_category and item_name and item_description:
            new_item = Item(category_name=item_category,
                            name=item_name,
                            description=item_description,
                            user_id=1)
            session.add(new_item)
            flash("New item %s successfully created." % new_item.name,
                  "alert-success")
            session.commit()
            return redirect(url_for("index"))
        else:
            flash("""Some fields were left blank.
                  Please enter the item details again.""",
                  "alert-danger")
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/<category>/<item>/edit", methods=["GET", "POST"])
def edit_item(category, item):
    if request.method == "POST":
        item_category = request.form["item-category"]
        item_name = request.form["item-name"]
        item_description = request.form["item-description"]
        if item_category and item_name and item_description:
            edited_item = session.query(Item).filter_by(category_name=category,
                                                        name=item_name).one()
            edited_item.category_name = item_category
            edited_item.name = item_name
            edited_item.description = item_description
            session.add(edited_item)
            flash("Item %s successfully edited." % edited_item.name,
                  "alert-success")
            session.commit()
            return redirect(url_for("item",
                                    category=item_category, item=item_name))
        else:
            flash("""Some fields were left blank.
                  Please enter the item details again.""",
                  "alert-danger")
            return redirect(url_for("item",
                                    category=item_category, item=item_name))
    else:
        return redirect(url_for("index"))


@app.route("/<category>/<item>/delete", methods=["GET", "POST"])
def delete_item(category, item):
    if request.method == "POST":
        item_to_delete = session.query(Item).filter_by(category_name=category,
                                                       name=item).one()
        session.delete(item_to_delete)
        flash("Item %s successfully deleted." % item,
              "alert-success")
        session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))
