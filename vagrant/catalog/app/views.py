from flask import render_template, url_for, flash, redirect, request, make_response, jsonify
from flask import session as login_session
from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Category, Item, User
import random
import string
import httplib2
import json
import requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from app.user_helper import create_user, get_user_id


# allow access to login_session details from templates
app.jinja_env.globals['LOGIN_SESSION'] = login_session

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


@app.route('/login')
def showLogin():
    """Create anti-forgery state token
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in our
    # token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += login_session['username']

    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'], "alert-success")
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'], "alert-success")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Revoke a current user's token and reset their login_session
    """
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """Disconnect based on provider
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.", "alert-success")
        return redirect(url_for('index'))
    else:
        flash("You are not logged in", "alert-danger")
        return redirect(url_for('index'))


# Connect to the database and create the session.
engine = create_engine('sqlite:///app/itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    """Handler method for the homepage.

    Args:
        None

    Returns:
        Renders the public homepage for users who aren't logged in, and
        the authenticated homepage for those who are.
    """
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.created_at.desc()).limit(10).all()
    if 'username' not in login_session:
        return render_template("home.html",
                               curr_category="Latest Items",
                               categories=categories,
                               items=items)
    else:
        return render_template("home_auth.html",
                               curr_category="Latest Items",
                               categories=categories,
                               items=items)


@app.route("/<category>")
def category(category):
    """Handler method for the category view.

    Args:
        category (str): the selected category to display items for.

    Returns:
        Renders a listing of all of the items in the selected category.
    """
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_name=category).all()
    return render_template("category_list.html",
                           curr_category=category,
                           categories=categories,
                           items=items)


@app.route("/<category>/<item>")
def item(category, item):
    """Handler method for the item page.

    Args:
        category (str): the category of the selected item.
        item (str): the name of the selected item.
    Returns:
        Renders the public item page for users who aren't logged in, and
        the authenticated item page for those who are.
    """
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(category_name=category,
                                         name=item).first()
    user = session.query(User).filter_by(id=item.user_id).one()
    if "username" in login_session and login_session["user_id"] == user.id:
        return render_template("item_auth.html",
                               item=item,
                               categories=categories,
                               user=user)
    else:
        return render_template("item.html",
                               item=item,
                               categories=categories,
                               user=user)


@app.route("/newitem", methods=["GET", "POST"])
def new_item():
    """Handler for creating new items.

    Args:
        None

    Returns:
        Renders the homepage with a flash message.
        Redirects users to the homepage if they attempt to navigate here via a
        GET request or they are not logged in.
    """
    if request.method == "POST" and "username" in login_session:
        item_category = request.form["item-category"]
        item_name = request.form["item-name"]
        item_description = request.form["item-description"]
        if item_category and item_name and item_description:
            new_item = Item(category_name=item_category,
                            name=item_name,
                            description=item_description,
                            user_id=login_session["user_id"])
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
    """Handler for editing existing items.

    Args:
        None

    Returns:
        Renders the item page with a flash message.
        Redirects users to the homepage if they attempt to navigate here via a
        GET request or they are not logged in.
    """
    if request.method == "POST" and "username" in login_session:
        item_category = request.form["item-category"]
        item_name = request.form["item-name"]
        item_description = request.form["item-description"]
        if item_category and item_name and item_description:
            edited_item = session.query(Item).filter_by(category_name=category,
                                                        name=item_name).one()
            if login_session["user_id"] != edited_item.user_id:
                flash("Items can only be edited by their original creator.",
                      "alert-danger")
                return redirect(url_for("item",
                                        category=item_category,
                                        item=item_name))
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
    """Handler for deleting existing items.

    Args:
        category (str): the category of the item to delete.
        item (str): the name of the item to delete.

    Returns:
        Renders the homepage with a flash message confirming deletion.
        Redirects users to the homepage if they attempt to navigate here via a
        GET request or they are not logged in.
    """
    if request.method == "POST" and "username" in login_session:
        item_to_delete = session.query(Item).filter_by(category_name=category,
                                                       name=item).one()
        if login_session["user_id"] != item_to_delete.user_id:
            flash("Items can only be deleted by their original creator.",
                  "alert-danger")
            return redirect(url_for("index"))
        session.delete(item_to_delete)
        flash("Item %s successfully deleted." % item,
              "alert-success")
        session.commit()
    return redirect(url_for("index"))


@app.route('/<category>/JSON')
def category_json(category):
    """JSON endpoint for viewing items in a particular category.

    Args:
        category (str): the category of items to display in JSON format.

    Returns:
        All of the items in the selected category in JSON format.
    """
    items = session.query(Item).filter_by(
        category_name=category).all()
    return jsonify(Item=[i.serialize for i in items])
