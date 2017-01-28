from flask import render_template, url_for
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
