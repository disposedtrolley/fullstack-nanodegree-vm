from flask import render_template, url_for
from app import app
from models import categories, items


@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html",
                           curr_category="Latest Items",
                           categories=categories,
                           items=items)


@app.route("/<category>")
def category(category):
    filtered_items = [{"name": "Goggles", "category": "Snowboarding"},
                      {"name": "Snowboard", "category": "Snowboarding"}]
    return render_template("category_list.html",
                           curr_category=category,
                           categories=categories,
                           items=filtered_items)


@app.route("/<category>/<item>")
def item(category, item):
    selected_item = {"name": "Stick", "category": "Hockey", "description": "This is the description."}
    return render_template("item.html",
                           item=selected_item,
                           categories=categories)
