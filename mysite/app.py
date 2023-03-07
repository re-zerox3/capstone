from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/xElectricSheepx/mysite/capstone/mysite/databaseForm.db'
app.config['SECRET_KEY'] = 'thisIsASecretyKeyThatWontWork'

db = SQLAlchemy(app)

####Classes for the different data types######

####user class - may not use
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    #planes = db.relationship('Planes', backref='user')

####inspection class
class Inspection(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicleNum = db.Column(db.String(8))
    todaysDate = db.Column(db.String(10))
    returnDate = db.Column(db.String(10))
    requester = db.Column(db.String(40))
    department = db.Column(db.String(40))
    destination = db.Column(db.String(80))
    beginODO = db.Column(db.String(40))
    comments = db.Column(db.String(150))
    operator = db.Column(db.String(40))
    completed = db.Column(db.String(40))

####Mileage class
class Mileage(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(20),nullable=False)
    beginMileage = db.Column(db.Integer)
    endMileage = db.Column(db.Integer)
    totalMiles = db.Column(db.Integer)
    driverName = db.Column(db.String(40), nullable=False)
    signature = db.Column(db.String(40), nullable=False)
    comments =  db.Column(db.String(40), nullable=False)
    plateNumber = db.Column(db.String(40), nullable=False)
    destination = db.Column(db.String(40), nullable=False)
    course = db.Column(db.String(40), nullable=False)    

####Available Class
class Available():
    License_Plate = db.Column(db.String,primary_key=True) 
    Vehicle_Name = db.Column(db.String(40),nullable=False)
    availability = db.Column(db.String(10),nullable=False)


#work in progress
'''
class Request(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(40))
    name = db.Column(db.String(40))
    dept = db.Column(db.String(40))
    courseNum = db.Column(db.Integer)
    phoneNum = db.Column(db.String(40))
    vanNum = db.Column(db.Integer)
    explorerNum = db.Column(db.Integer)
    suburbanNum = db.Column(db.Integer)
    equipment = db.Column(db.String(150))
    lands = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    participantsNum = db.Column(db.String(50))
    tripPurpose = db.Column(db.String(50))
    pickupDate = db.Column(db.String(40))
    pickupTime = db.Column(db.String(40))
    returnDate = db.Column(db.String(40))
    returnTime = db.Column(db.String(40))
    operator1 = db.Column(db.String(40))
    operator2 = db.Column(db.String(40))
    operator3 = db.Column(db.String(40))
    operator4 = db.Column(db.String(40))
    operator5 = db.Column(db.String(40))
    indexNum = db.Column(db.String(40))
    accountNum = db.Column(db.String(40))
    estMilesCost = db.Column(db.String(40))
'''

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

'''
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
'''



## @app.route('/inspection_form/?qrcode = ) -  this is the first route visited by someone checking out a vehicle must be accessed by a parameterized get request from the QR code
# GET request displays the inspection form with license plate already filled in
# POST request inserts new record in the inspection table, redirects to the mileage1 route /mileage_form/?qrcode=xyz123
@app.route('/inspection_form',methods=["GET","POST"])
def inspection():
    if request.method=="POST":
        # vehicleNum = request.form['vehicle #']
        vehicleNum = request.args.get('qrcode', '')
        todaysDate = request.form['todays date']
        returnDate = request.form['return date']
        requester = request.form['vehicle requster']
        department = request.form['Department']
        destination = request.form['Destination']
        beginODO = request.form['beginODO']
        comments = request.form['comments']
        operator = request.form['Operator']
        completed = "inspection completed"
        inspection1 = Inspection(vehicleNum=vehicleNum, todaysDate=todaysDate, returnDate=returnDate, requester=requester, department=department, destination=destination, beginODO=beginODO, comments=comments, operator=operator, completed=completed)
        db.session.add(inspection1)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('inspection_form.html')

# @app.route('/mileage_form1/?qrcode = ') - this is second route visited by someone checking out a vehicle and follows after the inspection form page
# GET displays the 1st mileage form with license plate already filled in
# POST request creates a new record in the mileage table and updates specific van in the available table to checked out, redirects to /mileage_form_2/?qrcode = 
@app.route('/mileageForm_1',methods=["GET","POST"])
def mileage1():
    if request.method=="POST":
        plateNumber = request.form['plateNumber']
        print(plateNumber)
        destination = request.form['destination']
        print(destination)
        course = request.form['course']
        print(course)
        departure = request.form['departure']
        print(departure)
        beginMileage = request.form['beginMileage']
        print(beginMileage)
        driverName = request.form['driverName']
        print(driverName)
        signature = request.form['signature']
        print(signature)
        comments = request.form['comments']
        print(comments)
        mileage1 = Mileage(plateNumber=plateNumber,course=course,destination=destination,departure=departure,beginMileage=beginMileage, driverName=driverName,signature=signature,comments=comments)
        db.session.add(mileage1)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("mileage_1.html")
    


# @app.route('/mileage_form2/?qrcode = ') - this is first route visited by someone checking in a vehicle and follows after the 1st milegae form
# GET displays the 2nd mileage form with license plate already filled in
# POST request updates a record in the mileage table and updates specific van in the available table to checked in, redirects to '/'
@app.route('/mileageForm_2', methods=["POST","GET"])
def mileage2():
    if request.method == "POST":
        print("hello world")
        departure = request.form['departure']
        print("departure:",departure)
   
        beginMileage = request.form['beginMileage']
        print("beginM:",beginMileage)
    
        endMileage = request.form['endMileage']
        print("bMIles:",endMileage)

        totalMiles= request.form['totalMiles']
        print("total:",totalMiles)

        driverName = request.form['driverName']
        print("driverName:",driverName)
    
        plateNumber = request.form['plateNumber']
        print("plateNum:",plateNumber)
    
        destination = request.form['destination']
        print("destination:",destination)
    
        course = request.form['course']
        print("course:",course)
    
        signature = request.form['signature']
        print("signature:",signature)
    
        comments = request.form['comments']
        print("comments:",comments)
    
        mileage = Mileage(departure=departure, beginMileage=beginMileage, endMileage=endMileage, totalMiles=totalMiles, driverName=driverName, 
                     plateNumber=plateNumber, destination=destination, course=course, signature=signature,comments=comments)
        db.session.add(mileage)
        db.session.commit()
        return redirect('/')
    else:
        plateNumber = request.form['plateNumber']
        updateMileage = Mileage.query.filter_by(plateNumber=plateNumber).first()

        return render_template('mileage.html')

## @app.route('/request_form') -  this is where Holly and end users can fill out a request for the vehicles necessary
# GET request displays a web page for filling out the form
# POST request updates the request table by inserting a new record in the request table in thee database
@app.route('/request_form')
#@login_required - not needed right now
def tsvr_form():
    return render_template('tsvr_form.html', userAuth=current_user.is_authenticated)


# @app.route('/view_entries') - this is a "home page" for nickie - contains a nav bar to navigate to the following routes:
#   1. /view_request_list 2. /view_inspection_list 3. /view_available 4. /view_mileage_list
# These are the four main routes for viewing the van data
# Note these are the only the list view of the data
# supports only GET method returns a basic nav page with a tags to navigate routes (see above ^^)
@app.route('/view_entries')
@login_required
def viewEntries():
    return render_template('viewEntries.html')

# @app.route('/view_request_list') - this is a page where nickie can view a list view of the active requests in the database
# The HTML page will contain a few pieces of information (id, license plate, etc)
# id is an a tag that redirects to '/view_request_detail/id'
@app.route('/view_request_list')
@login_required
def viewEntries():
    return render_template('view_request_list.html')


#@app.route('/view_request_detail/id') -  this is where Nickie can view a detailed view of the active requests in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the request form
@app.route('/view_request_detail')
@login_required
def viewEntries():
    return render_template('view_request_detail.html')

# @app.route('/view_inspection_list') - this is a page where nickie can view a list view of the active inspection records in the database
# The HTML page will contain a few pieces of information (id, license plate, etc)
# id is an a tag that redirects to '/view_inspection_detail/id'
@app.route('/')
@login_required
def viewEntries():
    return render_template('view_inspection_list.html')

# @app.route('/view_inspection_detail/id') -  this is where Nickie can view a detailed view of the active inspection records in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the inspection form
@app.route('/view_inspection_detail')
@login_required
def viewEntries():
    return render_template('view_inspection_detail.html')

# #@app.route('/view_mileage_list) -  this is where Nickie can view a list view of the active mileage records in the database
# The html is of the specific record in the database (noted by the id)
# id is an a tag that redirects to '/view_mileage_detail/id'
@app.route('/view_mileage_list')
@login_required
def viewEntries():
    return render_template('view_mileage_list.html')

# @app.route('/view_mileage_detail/id') -  this is where Nickie can view a detailed view of the active mileage records in the database
# The html is of the specific record in the database (noted by the id)
# The page displays all the information that would've been in the inspection form
@app.route('/view_mileage_detail')
@login_required
def viewEntries():
    return render_template('view_mileage_detail.html')

# @app.route('/view_available') -  this is where Nickie can view the availability table in the database
# The html is a simple graphic that shows all vans in db as well as their status (available/checkedout)
# Most basic site just a quick way for Nickie to view the fleet
@app.route('/view_available')
@login_required
def viewEntries():
    return render_template('view_available.html')

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

if __name__ == '__main__':
    app.run()