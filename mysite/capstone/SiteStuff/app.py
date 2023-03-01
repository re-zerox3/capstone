from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/xElectricSheepx/mysite/database.db'
app.config['SECRET_KEY'] = 'thisIsASecretyKeyThatWontWork'

db = SQLAlchemy(app)

class Planes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(40))
    model = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(20))
    role = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    age = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    planes = db.relationship('Planes', backref='user')

#db.create_all()
#db.session.add(User(name='John Smith', age='45', username='admin', password='admin'))
#db.session.commit()

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@app.route('/')
def index():
    return render_template('home.html', userAuth=current_user.is_authenticated)

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

@app.route('/view_entries')
@login_required
def viewEntries():
    return render_template('viewEntries.html', queryList=Planes.query.filter_by(user_id=current_user.id).all(), userAuth=current_user.is_authenticated)

@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

if __name__ == '__main__':
    app.run()