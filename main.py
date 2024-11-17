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
from forms import (
    AddStationForm ,
    VisualInspection,
    KaptonGluing,
    HvIvForm,
    SensorGluing,
    NeedleMetrologyForm,
    SkeletonTestForm,
    HybridGluingForm,
    WireBondingForm,
    NoiseTestForm,
    BufNimForm
)
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["UPLOAD_FOLDER"]= "static/uploads/station_image"
ckeditor = CKEditor(app)
Bootstrap5(app)
# CREATE DATABASE


class Base(DeclarativeBase):
    pass

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "nisers.db")}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB

class User(UserMixin, db.Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Primary key as Integer
    username: Mapped[str] = mapped_column(String(100), unique=True)  # Username as a unique field
    password: Mapped[str] = mapped_column(String(100))           # Password field
    name: Mapped[str] = mapped_column(String(100))              # Name field
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)  # Timestamp
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Boolean field for active status

    # Define a relationship to `Station` for reverse access if needed
    stations = relationship("Station", back_populates="user")

class Station(db.Model):
    __tablename__ = "Stations"
    id: Mapped[int] = mapped_column(Integer ,primary_key=True)
    station_name: Mapped[str] = mapped_column(String(100), nullable=False)
    station_location: Mapped[str] = mapped_column(String(100), nullable=False)
    remarks: Mapped[str]=mapped_column(String(4000))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)  # Timestamp
    img_path: Mapped[str]=mapped_column(String(1000), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Boolean field for active status
    iteration_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Link to the User table via the `username` field
    operator: Mapped[str] = mapped_column(String(100), ForeignKey("Users.username"), nullable=False)

    # Define the relationship to User for easy access to `User` attributes
    user = relationship("User", back_populates="stations")

# Flask log-in
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return db.get_or_404(User ,username)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for('secrets'))

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

@app.route('/secrets')
@login_required
def secrets():
    return render_template("home.html")
@app.route('/workflow')
@login_required
def work_flow():
    return render_template("workflow.html")

@app.route('/modules')
@login_required
def show_module():
    return render_template("modules.html")
@app.route('/module_report')
@login_required
def module_report():
    return render_template("module_report.html")



@app.route('/stations')
@login_required
def stations():
    with app.app_context():
        result = db.session.execute(db.select(Station).order_by(Station.id))
        all_stations = result.scalars().all()
        return render_template("all_stations.html",all_stations = all_stations)
    #return render_template("stations1.html")

@app.route("/station_form" ,methods=["GET","POST"])
@login_required
def show_form():
    form = AddStationForm()
    if form.validate_on_submit():
#    image = request.files["image"]
#    station_name = request.form["Station Name"]
#    station_location = request.form["Station Location"]
#    created_at = request.form["Created At"]
#    remarks = request.form["Remarks"]
#    img_path = os.path.join(app.config['UPLOAD_FOLDER'], station_img)
#    is_active = request.form["Is station active in this status"]
#    image.save(img_path)
#    print(img_path)
#    new_station = Station(station_name = station_name,
#                          station_location = station_location,
#                          remarks = remarks,
#                          created_at = created_at,
#                          img_path = img_path,
#                          is_active = is_active,
#                          iteration_number = iteration_number,
#                          operator = operator)
#    db.session.add(new_station)
#    db.session.commit()
#    return redirect(url_for('stations'))
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
        return redirect(url_for('stations'))
    return render_template("add_station_form.html",form = form)


@app.route("/add_station",methods=["POST"])
@login_required
def add_station():
    print("we have entered the upload_image")
    image = request.files["image"]
    station_name = request.form["Station Name"]
    station_location = request.form["Station Location"]
    created_at = request.form["Created At"]
    remarks = request.form["Remarks"]
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], station_img)
    is_active = request.form["Is station active in this status"]
    image.save(img_path)
    print(img_path)
    new_station = Station(station_name = station_name,
                          station_location = station_location,
                          remarks = remarks,
                          created_at = created_at,
                          img_path = img_path,
                          is_active = is_active,
                          iteration_number = iteration_number,
                          operator = operator)
    db.session.add(new_station)
    db.session.commit()
    return redirect(url_for('stations'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")

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
        form = BufNimForm()
    if form.validate_on_submit():
        # Handle the form submission logic here
        pass
    return render_template("visual_inspection.html", form=form)



if __name__ == "__main__":
    app.run(port=5555,debug=True)
