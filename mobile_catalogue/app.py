# -*- coding: utf-8 -*-
"""
    Mobile Catalogue
    ================
    A simple mobile catalogue app where Users can add mobile items to the site powered by SQLAlchemy/SQLite
"""
from flask import Flask, request, session, redirect, url_for, \
    render_template, flash, make_response
from modals import db, Category, MobileItem, ItemField, User
import requests
import json
import uuid
import hmac
from oauth2client import client
import datetime
import os

app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=str(uuid.uuid4()),
    #    SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
    SQLALCHEMY_DATABASE_URI='postgresql://catalog:catalog@localhost/appdb',
))
app.permanent_session_lifetime = datetime.timedelta(days=3)
db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    initdb()


def initdb():
    """Creates the database tables."""
    db.create_all()


@app.teardown_appcontext
def close_db(error=None):
    """Closes the database again at the end of the request."""
    db.session.remove()


# not using flask.session for storing cookies as they are gettting changes after ajax requests
# @app.before_first_request
# def make_cookie_perma():
#     print '# make cookies permanent'
#     session.permanent = True

def getHashForUserid(username):
    return hmac.new(str(username), '9b107808-372e-430c-bc0d-47f2b44e6dad').hexdigest()


def checkCookieHash(cookie_dict):
    """
    check if the userhash and username matches
    Args:
        cookie_dict (dict): a ditionary object with username and userhash keys
    Returns (bool): check for user tampering with cookies set
    """

    return cookie_dict.get('username') \
           and cookie_dict.get('userhash') \
           and cookie_dict.get('userhash') == getHashForUserid(cookie_dict.get('username'))


@app.route('/callback')
def gplus_connect():
    # initiating flow object
    flow = client.flow_from_clientsecrets(
        (os.path.join(os.path.abspath(os.path.dirname(__file__)), 'client_secrets.json')),
        scope='openid email',
        redirect_uri=url_for('gplus_connect', _external=True)
    )
    # first step: redirect to google page for authorisation
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    # got authorisation from google page
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    session['credentials'] = credentials.to_json()
    # get the user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    userinfo = requests.get(userinfo_url, params=params).json()

    # insert an user object if it doesn't exist in our database already
    user = User.query.filter_by(name=userinfo['name']).first()
    if not user:
        user = User(userinfo['name'], userinfo['email'], userinfo['picture'])
        db.session.add(user)
        db.session.commit()
    session['username'] = userinfo['name']
    resp = make_response(redirect(url_for('all_categories')))
    # used by angularjs
    cookie_lifetime = datetime.datetime.now() + app.permanent_session_lifetime
    resp.set_cookie('username', userinfo['name'], expires=cookie_lifetime)
    resp.set_cookie('userhash', getHashForUserid(userinfo['name']), expires=cookie_lifetime)
    return resp


@app.route('/', methods=['GET'])
def all_categories():
    user = None
    if checkCookieHash(request.cookies):
        user = User.query.filter_by(name=request.cookies['username']).first()
    if request.args.get('json') == 'all':
        # send all items in all categories
        ctgrys = []
        for ctgry in Category.query.all():
            ctgrys.append(ctgry.to_dict())
        return json.dumps(ctgrys)
    elif request.args.get('json') == 'titles':
        # send only category titles
        return json.dumps([ctgry.name for ctgry in Category.query.all()])
    elif request.args.get('json') == 'category' and request.args.get('category'):
        # return all items in a category
        ctgry = Category.query.filter_by(name=request.args.get('category')).first()
        if ctgry:
            return json.dumps(ctgry.to_dict())
    return render_template('index.html', user=user)


@app.route('/item', methods=['PUT', 'DELETE'])
def mobile_item():
    if not checkCookieHash(request.cookies):
        return json.dumps(dict(error="User must be logged-in."))

    user = User.query.filter_by(name=request.cookies['username']).first()
    if not user:
        return json.dumps(dict(error="Username is not found."))

    data = json.loads(request.data)  # type: dict
    ctgryObj = Category.query.filter_by(name=data['category']).first()
    item = MobileItem.query.filter_by(name=data['itemName'], category=ctgryObj).first()  # type:MobileItem
    if request.method == 'PUT':
        # add new mobile item or edit an existing one

        if not ctgryObj:
            # create a new category
            ctgryObj = Category(data['category'])
            db.session.add(ctgryObj)

        if item:
            # check for user
            if item.user != user:
                return json.dumps(dict(error="User is not authorised to edit this item."))
            # edit an existing item
            item.img = data['imgurl']
            item.category = ctgryObj
        else:
            # create a new item
            item = MobileItem(data['itemName'], data['imgurl'], ctgryObj, user)
            db.session.add(item)

        # add details to that item
        for fld in data['fields']:
            f = ItemField(fld['name'], fld['value'], item)
            db.session.add(f)
        db.session.commit()
        return json.dumps(dict(success="Mobile item is created successfully."))
    elif request.method == 'DELETE':
        # delete a mobile item from database using its name
        if not ctgryObj:
            return json.dumps(dict(error="No such category found."))
        if not item:
            return json.dumps(dict(error="No such item found."))
        if item.user != user:
            return json.dumps(dict(error="User is not authorised to delete this item."))
        db.session.delete(item)
        db.session.commit()
        return json.dumps(dict(success="Mobile item is deleted successfully."))


@app.route('/signout')
def signout():
    # clearout all cookie values
    session.clear()
    resp = make_response(redirect(url_for('all_categories')))
    # unset cookie
    resp.set_cookie('username', expires=0)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
