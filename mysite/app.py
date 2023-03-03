from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/xElectricSheepx/mysite/capstone/mysite/databaseForm.db'
app.config['SECRET_KEY'] = 'thisIsASecretyKeyThatWontWork'

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    #planes = db.relationship('Planes', backref='user')

#db.create_all()
#db.session.add(User(name='John Smith', age='45', username='admin', password='admin'))
#db.session.commit()

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


#######Capstone Routes#########

# @app.route('/') - this is the home route,
# This HTML template can be a nav homescreen
# a tags to the following routes, /login (for nickie) /request_form (for holly... and the like)
# we will change this page to reflect comments
@app.route('/')
def index():
    return render_template('home.html', userAuth=current_user.is_authenticated)

# @app.route('/login') - this is the home route, also the login route for nickie to have access to all the read routes
# This HTML template can be a simple login form
# GET displays login form
# POST redirects to /view_entries
@app.route('/login', methods=['GET','POST'])
def login():
    formSuccess = True
    if request.method == 'GET':
        return render_template('loginForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        formSuccess = False
        return render_template('loginForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    if user.password == password:
        login_user(user)
        return render_template('home.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)

# @app.route('/logout') - visitng this route logs out user
# Logs Nickie out of the webapp
# redirects to '/'
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html', userAuth=current_user.is_authenticated)

@app.route('/create_user', methods=['GET', 'POST'])
def create():
    formSuccess = True
    if request.method == 'GET':
        return render_template('createForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    name = request.form['name']
    age = request.form['age']
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        db.session.add(User(name=name, age=age, username=username, password=password))
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return render_template('home.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    elif user is not None:
        formSuccess = False
        return render_template('createForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)

@app.route('/update_user', methods=['GET','POST'])
@login_required
def update():
    formSuccess = True
    if request.method == 'GET':
        return render_template('updateForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    oldPassword = request.form['oldPassword']
    newPassword = request.form['newPassword']
    if current_user.password != oldPassword:
        formSuccess = False
        return render_template('updateForm.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    elif current_user.password == oldPassword:
        current_user.password = newPassword
        db.session.commit()
        return render_template('home.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)

@app.route('/view_user')
@login_required
def viewUser():
    return render_template('viewUserInfo.html', userQuery=User.query.filter_by(id=current_user.id).first(), userAuth=current_user.is_authenticated)


## @app.route('/inspection_form/?qrcode = ) -  this is the first route visited by someone checking out a vehicle must be accessed by a parameterized get request from the QR code
# GET request displays the inspection form with license plate already filled in
# POST request inserts new record in the inspection table, redirects to the mileage1 route /mileage_form/?qrcode =
@app.route('/inspection_form')
#@login_required - not needed right now
def inspection():
    return render_template('inspectionForm.html', userAuth=current_user.is_authenticated)


# @app.route('/mileage_form1/?qrcode = ') - this is second route visited by someone checking out a vehicle and follows after the inspection form page
# GET displays the 1st mileage form with license plate already filled in
# POST request creates a new record in the mileage table and updates specific van in the available table to checked out, redirects to /mileage_form_2/?qrcode =
@app.route('/mileage_form1')
#@login_required - not needed right now
def mileage_1():
    return render_template('mileage_1.html', userAuth=current_user.is_authenticated)


# @app.route('/mileage_form2/?qrcode = ') - this is first route visited by someone checking in a vehicle and follows after the 1st milegae form
# GET displays the 2nd mileage form with license plate already filled in
# POST request updates a record in the mileage table and updates specific van in the available table to checked in, redirects to '/'
@app.route('/mileage_form2')
#@login_required - not needed right now
def mileage_2():
    return render_template('mileage_2.html', userAuth=current_user.is_authenticated)


## @app.route('/request_form') -  this is where Holly and end users can fill out a request for the vehicles necessary
# GET request displays a web page for filling out the form
# POST request updates the request table by inserting a new record in the request table in thee database
@app.route('/request_form')
#@login_required - not needed right now
def tsvr_form():
    return render_template('tsvr_form.html', userAuth=current_user.is_authenticated)

'''
@app.route('/create_entries', methods=['GET','POST'])
@login_required
def createEntries():
    formSuccess = True
    if request.method == 'GET':
        return render_template('createEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    planeMaker = request.form['manufacturer']
    planeModel = request.form['model']
    planeAmount = request.form['amount']
    planeType = request.form['type']
    planeRole = request.form['role']
    uniqueCheck = queryList=Planes.query.filter_by(model=planeModel, user_id=current_user.id).first()
    if planeModel is not None and uniqueCheck is None:
        newPlane = Planes(manufacturer=planeMaker, model=planeModel, amount=planeAmount, type=planeType, role=planeRole)
        newPlane.user = current_user
        db.session.add(newPlane)
        db.session.commit()
        return render_template('createEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    elif planeModel or uniqueCheck is None:
        formSuccess = False
        return render_template('createEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
@app.route('/update_entries', methods=['GET','POST'])
@login_required
def updateEntries():
    formSuccess = True
    if request.method == 'GET':
        return render_template('updateEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    planeModel = request.form['model']
    updateModel = Planes.query.filter_by(model=planeModel, user_id=current_user.id).first()
    if updateModel is not None:
        updateModel.manufacturer = request.form['manufacturer']
        updateModel.amount = request.form['amount']
        updateModel.type = request.form['type']
        updateModel.role = request.form['role']
        db.session.commit()
        return render_template('updateEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    elif updateModel is None:
        formSuccess = False
        return render_template('updateEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
@app.route('/delete_entries', methods=['GET','POST'])
@login_required
def deleteEntries():
    formSuccess = True
    if request.method == 'GET':
        return render_template('deleteEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    planeModel = request.form['model']
    entry = Planes.query.filter_by(model=planeModel, user_id=current_user.id).first()
    if entry is not None:
        db.session.delete(entry)
        db.session.commit()
        return render_template('deleteEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    elif entry is None:
        formSuccess = False
        return render_template('deleteEntries.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
'''
# @app.route('/view_entries') - this is a "home page" for nickie - contains a nav bar to navigate to the following routes:
#   1. /viewrequestlist 2. /viewinspectionlist 3. /viewavailable 4. /viewmileagelist
# These are the four main routes for viewing the van data
# Note these are the only the list view of the data
# supports only GET method returns a basic nav page with a tags to navigate routes (see above ^^)
@app.route('/view_entries')
@login_required
def viewEntries():
    return render_template('viewEntries.html', queryList=Planes.query.filter_by(user_id=current_user.id).all(), userAuth=current_user.is_authenticated)

# @app.route('/view_request_list') - this is a page where nickie can view a list view of the active requests in the database
# The HTML page will contain a few pieces of information (id, license plate, etc)
# id is an a tag that redirects to '/view_request_detail/id'

#@app.route('/view_request_detail/id') -  this is where Nickie can view a detailed view of the active requests in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the request form

# @app.route('/view_inspection_list') - this is a page where nickie can view a list view of the active inspection records in the database
# The HTML page will contain a few pieces of information (id, license plate, etc)
# id is an a tag that redirects to '/view_inspection_detail/id'

# @app.route('/view_inspection_detail/id') -  this is where Nickie can view a detailed view of the active inspection records in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the inspection form

# #@app.route('/view_mileage_list) -  this is where Nickie can view a list view of the active mileage records in the database
# The html is of the specific record in the database (noted by the id)
# id is an a tag that redirects to '/view_mileage_detail/id'

# @app.route('/view_mileage_detail/id') -  this is where Nickie can view a detailed view of the active mileage records in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the inspection form

# @app.route('/view_available') -  this is where Nickie can view the availability table in the database
# The html is a simple graphic that shows all vans in db as well as their status (available/checkedout)
# Most basic site just a quick way for Nickie to view the fleet

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

if __name__ == '__main__':
    app.run()