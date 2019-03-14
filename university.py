from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from university_db import University, Base, College, User
from flask import session as login_session
import random
import string
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "University College item-catalog"
engine = create_engine(
    'sqlite:///university.db', connect_args={'check_same_thread': False},
    echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# For User login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current state is %s" %login_session['state']
    university = session.query(University).all()
    college = session.query(College).all()
    return render_template('login.html', STATE=state, university=university,
                           college=college)


# If User already logged
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                 json.dumps(
                                            'Current user already connected'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<center><h2><font color="green">Welcome '
    output += login_session['username']
    output += '!</font></h2></center>'
    output += '<center><img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; -webkit-border-radius: 200px;" '
    output += ' " style = "height: 200px;border-radius: 200px;" '
    output += ' " style = "-moz-border-radius: 200px;"></center>" '
    flash("you are now logged in as %s" % login_session['username'])
    print("Done")
    return output


# Create New User
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Getting information of user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Getting user email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# To read university JSON data on web browser
@app.route('/university/JSON')
def universityJSON():
    university = session.query(University).all()
    return jsonify(university=[u.serialize for u in university])


# To read university wise of college JSON
@app.route('/university/<int:university_id>/menu/<int:college_id>/JSON')
def universityListJSON(university_id, college_id):
    College_List = session.query(College).filter_by(id=college_id).one()
    return jsonify(College_List=College_List.serialize)


# To read colleges JSON
@app.route('/university/<int:college_id>/menu/JSON')
def collegeListJSON(college_id):
    university = session.query(University).filter_by(id=college_id).one()
    college = session.query(College).filter_by(college_id=university.id).all()
    return jsonify(CollegeLists=[i.serialize for i in college])


# This is a home page of entire project
@app.route('/university/')
def showUniversity():
    university = session.query(University).all()
    return render_template('university.html', university=university)


# Create new University
@app.route('/university/new/', methods=['GET', 'POST'])
def newUniversity():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newUniversity = University(name=request.form['name'],
                                   user_id=login_session['user_id'])
        session.add(newUniversity)
        session.commit()
        return redirect(url_for('showUniversity'))
    else:
        return render_template('newUniversity.html')


# To Editing existing university name
@app.route('/university/<int:university_id>/edit/', methods=['GET', 'POST'])
def editUniversity(university_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedUniversity = session.query(University).filter_by(
                                     id=university_id).one()
    creater_id = getUserInfo(editedUniversity.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this University "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showUniversity'))
    if request.method == 'POST':
        if request.form['name']:
            editedUniversity.name = request.form['name']
            flash(
                "University Successfully Edited %s" % (editedUniversity.name))
            return redirect(url_for('showUniversity'))
    else:
        return render_template(
                    'editedUniversity.html', university=editedUniversity)


# To Deleting existing University
@app.route('/university/<int:university_id>/delete/', methods=['GET', 'POST'])
def deleteUniversity(university_id):
    if 'username' not in login_session:
        return redirect('/login')
    universityToDelete = session.query(University).filter_by(
                                       id=university_id).one()
    creater_id = getUserInfo(universityToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot delete this University "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showUniversity'))
    if request.method == 'POST':
        session.delete(universityToDelete)
        flash("Successfully Deleted %s" % (universityToDelete.name))
        session.commit()
        return redirect(url_for('showUniversity', university_id=university_id))
    else:
        return render_template(
            'deleteUniversity.html', university=universityToDelete)


# It's Displays the total College list of partcular university
@app.route('/university/<int:university_id>/colleges')
def showCollege(university_id):
    university = session.query(University).filter_by(id=university_id).one()
    college = session.query(College).filter_by(college_id=university_id).all()
    return render_template('menu.html', university=university, college=college)


# Creating new college
@app.route('/university/<int:college_id>/new/', methods=['GET', 'POST'])
def newCollegeList(college_id):
    if 'username' not in login_session:
        return redirect('login')
    university = session.query(University).filter_by(id=college_id).one()
    creater_id = getUserInfo(university.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot add this college "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showUniversity', university_id=college_id))
    if request.method == 'POST':
        newList = College(
                           name=request.form['name'],
                           address=request.form['address'],
                           founded=request.form['founded'],
                           phone=request.form['phone'],
                           place=request.form['place'],
                           college_id=college_id,
                           user_id=login_session['user_id']
                          )
        session.add(newList)
        session.commit()
        flash("New College List %s is created" % (newList))
        return redirect(url_for('showCollege', university_id=college_id))
    else:
        return render_template('newcollegelist.html', college_id=college_id)


# Editing to particular university college
@app.route('/university/<int:university_id>/<int:c_id>/edit/',
           methods=['GET', 'POST'])
def editCollegeList(university_id, c_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedList = session.query(College).filter_by(id=c_id).one()
    university = session.query(University).filter_by(id=university_id).one()
    creater_id = getUserInfo(editedList.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this University "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showCollege', university_id=university_id))
    if request.method == 'POST':
        editedList.name = request.form['name']
        editedList.address = request.form['address']
        editedList.founded = request.form['founded']
        editedList.phone = request.form['phone']
        editedList.place = request.form['place']
        session.add(editedList)
        session.commit()
        flash("College List has been edited!!")
        return redirect(url_for('showCollege', university_id=university_id))
    else:
        return render_template('editcollegelist.html',
                               university=university, college=editedList)


# Deleting particular university of college
@app.route('/university/<int:college_id>/<int:list_id>/delete/',
           methods=['GET', 'POST'])
def deleteCollegeList(college_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    university = session.query(University).filter_by(id=college_id).one()
    listToDelete = session.query(College).filter_by(id=list_id).one()
    creater_id = getUserInfo(listToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this university "
              "This is belongs to %s" % (creater_id.name))
        # return redirect(url_for('showColleges', university_id=college_id))
    if request.method == 'POST':
        session.delete(listToDelete)
        session.commit()
        flash("College list has been Deleted!!!")
        return redirect(url_for('showCollege', university_id=college_id))
    else:
        return render_template('deletecollegelist.html', lists=listToDelete)


# Logout from application
@app.route('/disconnect')
def logout():
    access_token = login_session['access_token']
    print("In gdisconnect access token is %s", access_token)
    print("User Name is:")
    print(login_session['username'])

    if access_token is None:
        print("Access Token is None")
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out")
        return redirect(url_for('showUniversity'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
