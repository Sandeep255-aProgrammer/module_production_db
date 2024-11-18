from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Boolean, DateTime
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
import os
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import datetime


''' 
below  import all the forms required , which is defined in the forms.py
''' 

from forms import (
    AddStationForm ,
    MaterialReceiver,
    VisualInspection,
    KaptonGluing,
    HvIvForm,
    SensorGluing,
    NeedleMetrologyForm,
    SkeletonTestForm,
    HybridGluingForm,
    WireBondingForm,
    NoiseTestForm,
    BurNimForm
)



''' 
now import all the stups related to the database tike the table and db , all are defined in the database_table.html

'''

from database_table import User , Station , db



'''
  create the flask object and follow some rules
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["UPLOAD_FOLDER"]= "static/uploads/station_image"
ckeditor = CKEditor(app)
Bootstrap5(app)

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "nisers.db")}'
db.init_app(app)



#Flask log-in  ,this part is crucial for authenticaton 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return db.get_or_404(User ,username)

# create all the tables 

with app.app_context():
    db.create_all()


# this is the home part for unauthenticated user
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for('secrets'))

# login part login.html is rendered 
@app.route('/login',methods =["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Query the Users table based on the username
        result = db.session.execute(db.select(User).where(User.username == username))
        user = result.scalar()
        # Check if user exists and is active
        if user:
            if not user.is_active:
                flash("Your account is inactive. Please contact support.")
                return redirect(url_for('login'))

            # Verify password
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                flash("Incorrect password, please try again.")
        else:
            flash("User does not exist, please check your email.")
    return render_template("login.html")

# once the user is authenticated this is the home page , home.html is rendered 
@app.route('/secrets')
@login_required
def secrets():
    return render_template("home.html")

# when you click on the workflow button in the home page this method is called and workflow.html is rendered 
@app.route('/workflow')
@login_required
def work_flow():
    return render_template("workflow.html")

# when you click on the modules in the homepage this method is called and modules.html is rendered 
@app.route('/modules')
@login_required
def show_module():
    return render_template("modules.html")

# when you click on a specific module id this method is executed and module_report.html corresponding to that module will# be rendered and it is under ..
@app.route('/module_report')
@login_required
def module_report():
    return render_template("module_report.html")


'''
 this portion is the activated when stations is clicked basically it shows all the stations that are available in the database and gives a options to add more stations 
'''

@app.route('/stations')
@login_required
def stations():
    print(current_user.username)
    with app.app_context():
        result = db.session.execute(db.select(Station).order_by(Station.id))
        all_stations = result.scalars().all()
        return render_template("all_stations.html",all_stations = all_stations,user_name = current_user.username)
    #return render_template("stations1.html")
'''
This show_form functions adds the new station to the database and redirect to the the method stations page after successfull completion 

'''
@app.route("/station_form" ,methods=["GET","POST"])
@login_required
def show_form():
    form = AddStationForm()
    if form.validate_on_submit():
        f = form.station_img.data
        station_name = form.station_name.data
        station_location = form.station_location.data
        station_created_at = form.station_created_at.data
        station_remarks = form.station_remarks.data
        #img_path = os.path.join(app.config['UPLOAD_FOLDER'], station_img)
        station_is_active = form.station_is_active.data
        station_iteration_number = form.station_iteration_number.data
        station_operator = form.station_operator.data
        filename = secure_filename(f.filename)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(os.path.join(img_path))
        new_station = Station(station_name = station_name,
                              station_location = station_location,
                              created_at = station_created_at,
                              remarks = station_remarks,
                              img_path = img_path,
                              is_active = station_is_active,
                              iteration_number = station_iteration_number,
                              operator = station_operator)
        db.session.add(new_station)
        db.session.commit()
        return redirect(url_for('stations'))
    if current_user.is_authenticated:
        form.station_operator.data = current_user.username  # Set station_operator to current user's name
        form.station_operator.render_kw = {'readonly': True}
    return render_template("add_station_form.html",form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# this part meant for downloding the report corresponding to a perticular module
@app.route('/download')
@login_required
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")


'''
 here the main thing comes , in the workflow page when you select a process , the num gets it's value which is defined in the workflow.html have a look , that number will tell(see the logic below)  which form to show and after we have to save the data entered in the form to the database once the form is validated 
  Also the visual_inspection.html renders the form
''' 

@app.route('/add_data', methods=["GET", "POST"])
def add_data():
    num = request.args.get('num')
    step_no = int(num)
    if step_no == 0:
        form = MaterialReceiver()
    elif step_no == 1:
        form = VisualInspection()
    elif step_no == 2:
        form = KaptonGluing()
    elif step_no == 3:
        form = HvIvForm()
    elif step_no == 4:
        form = SensorGluing()
    elif step_no == 5:
        form = NeedleMetrologyForm()
    elif step_no == 6:
        form = SkeletonTestForm()
    elif step_no == 7:
        form = HybridGluingForm()
    elif step_no == 11:
        form = ModuleData()
    elif step_no == 8:
        form = WireBondingForm()
    elif step_no == 9:
        form = NoiseTestForm()
    elif step_no == 10:
        form = BurNimForm()
    if form.validate_on_submit():
        # Handle the form submission logic here
        pass
    return render_template("visual_inspection.html", form=form)



if __name__ == "__main__":
    app.run(port=5555,debug=True)
