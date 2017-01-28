from flask import render_template, url_for
from app import app
from models import categories, items


@app.route('/')
@app.route('/index')
def index():
    return render_template("home_auth.html",
                           curr_category="Latest Items",
                           categories=categories,
                           items=items)


@app.route("/<category>")
def category(category):
    filtered_items = []
    for x in items:
        if x.get("category") == category:
            filtered_items.append(x)
    return render_template("category_list.html",
                           curr_category=category,
                           categories=categories,
                           items=filtered_items)


@app.route("/<category>/<item>")
def item(category, item):
    selected_item = None
    for x in items:
        if x.get("name") == item:
            selected_item = x
    return render_template("item_auth.html",
                           item=selected_item,
                           categories=categories)
