from flask import *
from flask import request
from flask_sqlalchemy import *
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required


app = Flask(__name__, static_url_path='/static')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/xElectricSheepx/mysite/capstone/mysite/instance/databaseForm.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseForm.db'
app.config['SECRET_KEY'] = 'thisIsASecretyKeyThatWontWork'

db = SQLAlchemy(app)

####Classes for database tables######

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

class Inspections(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicleNum = db.Column(db.String(8), nullable=False)
    todaysDate = db.Column(db.String(10), nullable=False)
    returnDate = db.Column(db.String(10), nullable=False)
    requester = db.Column(db.String(40), nullable=False)
    department = db.Column(db.String(40), nullable=False)
    destination = db.Column(db.String(80), nullable=False)
    beginODO = db.Column(db.String(40), nullable=False)
    comments = db.Column(db.String(150), nullable=False)
    operator = db.Column(db.String(40), nullable=False)

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

class Available(UserMixin, db.Model):
    License_Plate = db.Column(db.String,primary_key=True)
    Vehicle_Name = db.Column(db.String(40),nullable=False)
    availability = db.Column(db.String(10),nullable=False)

class Requests(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    dept = db.Column(db.String(40), nullable=False)
    courseNum = db.Column(db.Integer, nullable=False)
    phoneNum = db.Column(db.String(40), nullable=False)
    vanNum = db.Column(db.Integer, nullable=False)
    explorerNum = db.Column(db.Integer, nullable=False)
    suburbanNum = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(150), nullable=False)
    lands = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    participantsNum = db.Column(db.Integer, nullable=False)
    tripPurpose = db.Column(db.String(50), nullable=False)
    pickupDate = db.Column(db.String(40), nullable=False)
    pickupTime = db.Column(db.String(40), nullable=False)
    returnDate = db.Column(db.String(40), nullable=False)
    returnTime = db.Column(db.String(40), nullable=False)
    operator1 = db.Column(db.String(40), nullable=False)
    operator2 = db.Column(db.String(40))
    operator3 = db.Column(db.String(40))
    operator4 = db.Column(db.String(40))
    operator5 = db.Column(db.String(40))
    indexNum = db.Column(db.String(40), nullable=False)
    accountNum = db.Column(db.String(40), nullable=False)
    estMilesCost = db.Column(db.String(40), nullable=False)

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
def home():
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

### Debugging Routes ###
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

## @app.route('/inspection_form/?code = ) -  this is the first route visited by someone checking out a vehicle must be accessed by a parameterized get request from the QR code
# GET request displays the inspection form with license plate already filled in
# POST request inserts new record in the inspection table, redirects to the mileage1 route /mileage_form/?code=xyz123
@app.route('/inspection_form', methods=["GET","POST"])
def inspection():
    if request.method=='POST':
        vehicleNum = request.form['vehicleNum']
        todaysDate = str(request.form['todaysdate'])
        returnDate = str(request.form['returndate'])
        requester = request.form['requester']
        department = request.form['department']
        destination = request.form['destination']
        beginODO = request.form['beginODO']
        comments = request.form['comments']
        operator = request.form['operator']

        inspection1 = Inspections(vehicleNum=vehicleNum, todaysDate=todaysDate, returnDate=returnDate, requester=requester, department=department, destination=destination, beginODO=beginODO, comments=comments, operator=operator)
        db.session.add(inspection1)
        db.session.commit()
        print("inspection post")
        return redirect('/')

    else:
        code = request.args.get('code') #// This is for later, need to implement QR code stuff.
        # args = request.args
        # code = request.args('code')
        print("code", code)
        return render_template('inspectionForm.html', vehicleNum=code)

# @app.route('/mileage_form1/?code = ') - this is second route visited by someone checking out a vehicle and follows after the inspection form page
# GET displays the 1st mileage form with license plate already filled in
# POST request creates a new record in the mileage table and updates specific van in the available table to checked out, redirects to /mileage_form_2/?code =
@app.route('/mileageForm1', methods=["GET","POST"])
def mileage1():
    #PRE: Renders a html to complete form
    #POST: Updates mileage Table based on platerNumber
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
        setAvailability1(plateNumber)
        mileage1 = Mileage(plateNumber=plateNumber,course=course,destination=destination,departure=departure,beginMileage=beginMileage, driverName=driverName,signature=signature,comments=comments)
        db.session.add(mileage1)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("mileage_1.html")


# @app.route('/mileage_form2/?code = ') - this is first route visited by someone checking in a vehicle and follows after the 1st milegae form
# GET displays the 2nd mileage form with license plate already filled in
# POST request updates a record in the mileage table and updates specific van in the available table to checked in, redirects to '/'
@app.route('/mileageForm2', methods=["POST","GET"])
def mileage2():
    #PRE: Retrieve data from Mileage Table
    #POST Updates Mileage Table and sets status for Available Table
    if request.method == "POST":
        mileageData = []
        print("hello world")

        departure = request.form['departure']
        print("departure:",departure)
        mileageData.append(departure)

        beginMileage = request.form['beginMileage']
        print("beginM:",beginMileage)
        mileageData.append(beginMileage)

        endMileage = request.form['endMileage']
        print("bMIles:",endMileage)
        mileageData.append(endMileage)

        totalMiles= request.form['totalMiles']
        print("total:",totalMiles)
        mileageData.append(totalMiles)

        driverName = request.form['driverName']
        print("driverName:",driverName)
        mileageData.append(driverName)

        plateNumber = request.form['plateNumber']
        print("plateNum:",plateNumber)
        mileageData.append(plateNumber)

        destination = request.form['destination']
        print("destination:",destination)
        mileageData.append(destination)

        course = request.form['course']
        print("course:",course)
        mileageData.append(course)

        signature = request.form['signature']
        print("signature:",signature)
        mileageData.append(signature)

        comments = request.form['comments']
        print("comments:",comments)
        mileageData.append(comments)
        mileageHelper(plateNumber,mileageData)
        return redirect('/')
    else:
        mileage = Mileage.query.filter_by(plateNumber="887TTX").first()
        print(mileage)
        return render_template('mileage2.html',departure=mileage.departure ,plateNumber=mileage.plateNumber,beginMileage=mileage.beginMileage,destination=mileage.destination,course=mileage.course,driverName=mileage.driverName,signature=mileage.signature,comments=mileage.comments)

def checkAvailability(plateNumber):
    availability = Available.query.filter_by(License_Plate="887TTX").first()
    print(availability.License_Plate)
    print(availability.Vehicle_Name)

def setAvailability1(plateNumber):
    available = Available.query.filter_by(License_Plate=plateNumber).first()
    available.availability = "Checked Out"
    db.session.commit()

def setAvailability2(plateNumber):
    available = Available.query.filter_by(License_Plate=plateNumber).first()
    available.availability = "CheckedIn"
    db.session.commit()

def mileageHelper(plateNumber,mileageDate):
    #PRE: Retrieve data based on plateNumber for update
    #POST:Updates Mileage Table
    mileage = Mileage.query.filter_by(plateNumber= plateNumber).first()
    mileage.departure= mileageDate[0]
    mileage.beginMileage=mileageDate[1]
    mileage.endMileage= mileageDate[2]
    mileage.totalMiles= mileageDate[3]
    mileage.driverName= mileageDate[4]
    mileage.plateNumber = mileageDate[5]
    mileage.destination = mileageDate[6]
    mileage.course = mileageDate[7]
    mileage.signature = mileageDate[8]
    mileage.comments = mileageDate[9]
    db.session.commit()

## @app.route('/request_form') -  this is where Holly and end users can fill out a request for the vehicles necessary
# GET request displays a web page for filling out the form
# POST request updates the request table by inserting a new record in the request table in thee database
@app.route('/request_form', methods=['GET','POST'])
def tsvr_form():
    formSuccess = True
    if request.method == 'GET':
        return render_template('tsvr_form.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)
    date = str(request.form['date'])
    name = request.form['name']
    dept = request.form['dept']
    courseNum = request.form['courseNum']
    phoneNum = request.form['phoneNum']
    vanNum = request.form['vanNum']
    explorerNum = request.form['explorerNum']
    suburbanNum = request.form['suburbanNum']
    equipment = request.form['equipment']
    lands = request.form['lands']
    destination = request.form['destination']
    participantsNum = request.form['participantsNum']
    tripPurpose = request.form['tripPurpose']
    pickupDate = str(request.form['pickupDate'])
    pickupTime = str(request.form['pickupTime'])
    returnDate = str(request.form['returnDate'])
    returnTime = str(request.form['returnTime'])
    operator1 = request.form['operator1']
    operator2 = request.form['operator2']
    operator3 = request.form['operator3']
    operator4 = request.form['operator4']
    operator5 = request.form['operator5']
    indexNum = request.form['indexNum']
    accountNum = request.form['accountNum']
    estMilesCost = request.form['estMilesCost']
    requestResult = Requests.query.filter_by(name=name).first()
    if requestResult is None:
        db.session.add(Requests(date=date, name=name, dept=dept, courseNum=courseNum, phoneNum=phoneNum, vanNum=vanNum, explorerNum=explorerNum, suburbanNum=suburbanNum, equipment=equipment, lands=lands,
            destination=destination, participantsNum=participantsNum, tripPurpose=tripPurpose, pickupDate=pickupDate, pickupTime=pickupTime, returnDate=returnDate, returnTime=returnTime, operator1=operator1, operator2=operator2, operator3=operator3,
            operator4=operator4, operator5=operator5, indexNum=indexNum, accountNum=accountNum, estMilesCost=estMilesCost))
        db.session.commit()
        return redirect('/')
    else:
        formSuccess = False
        return render_template('tsvr_form.html', userAuth=current_user.is_authenticated, formSuccess=formSuccess)

'''
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
'''

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

if __name__ == '__main__':
    app.run()
