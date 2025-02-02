from flask import Flask, session ,render_template, request,jsonify, url_for, redirect, flash, send_from_directory
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
import json
import datetime
from sqlalchemy import inspect
import csv
import json

utc_now = datetime.datetime.now()
current_date =f"{utc_now.year}-{utc_now.month}-{utc_now.day}" 
''' 
below  import all the forms required , which is defined in the forms.py
''' 


from forms import (
   
    AddStationForm ,
   
    SensorVisualForm ,
    FEHVisualForm,
   SEHVisualForm,
    MainBridgeVisualForm,
   StumpBridgeVisualForm,
    KaptonGluing,
    HvForm,
    IvForm ,
    SensorGluing,
    NeedleMetrologyForm,
    SkeletonTestForm,
    HybridGluingForm,
    ModuleEncapsulationForm ,
    WireBondingForm,
    NoiseTestForm_Ph2_ACF,
    NoiseTestForm_GIPHT
)
#      SensorForm  ,
#     VTRxIDForm ,VTRxForm,GroundBalancerIDForm ,  GroundBalancerForm,
#     FEHForm, SEHForm, MainBridgeForm, StumpBridgeForm, GlueForm, KaptonTapesForm, OpticalFibreForm, WireBonderForm, OtherConsumablesForm
#       ,SensorIdListForm, FEHIdListForm, SEHIdListForm, MainBridgeIdListForm, StumpBridgeIdListForm, GlueBatchIdListForm, KaptonTapeIdListForm, OpticalFibreIdListForm, WireBonderDetailsForm, JigIDForm , OtherConsumablesListForm
# )

# material_receiver_data_dict = [{"sensor_id":[]},{"FEH_id":[]},{"SEH_id":[]},
#                                {"main_bridge_id":[]},{"stump_bridge_id":[]},
#                                {"glue_batch_id":[],"glue_expiry_date":[]},{"kapton_id":[]},{"optical_fibre_id":[]},
#                                {"spool_no":[],"wedge_tool_no":[],"expiry_date":[]},{"jig_id":[]},{"other_id":[]}]
# current_material_data = material_receiver_data_dict[0]
# Material_receiver_ids_forms = [SensorIdListForm, FEHIdListForm, SEHIdListForm, MainBridgeIdListForm, StumpBridgeIdListForm, 
#                                GlueBatchIdListForm, KaptonTapeIdListForm, OpticalFibreIdListForm, WireBonderDetailsForm,  
#                                JigIDForm,OtherConsumablesListForm,VTRxIDForm,GroundBalancerIDForm]

''' 
now import all the stups related to the database tike the table and db , all are defined in the database_table.html

'''

#from database_table import User , Station , db
#TO DO: Need to change the import statement to import all the tables from database_table.py
from database_table1 import (db , UserTable , DateTimeTable , StationTable , TempHumiDewTable ,MaterialReceivingCommonTable , SensorTable , FEHTable , SEHTable , MainBridgeTable , StumpBridgeTable ,
KaptonTapeTable , OtherTable , VTRxTable , GroundBalancerTable , GlueTable , WireBonderTable,JigTable, VSensorTable, VFEHTable , VSEHTable,
VMainBridgeTable , VStumpBridgeTable , KaptonGluingTable , HVTable , IVTable , SensorGluingTable , NeedleMetrologyTable , SkeletonTestTable,
HybridGluingTable , ModuleEncapsulationTable , WireBondingTable , NoiseTestPh2ACFTable , NoiseTestGIPHTTable , BurninTestTable )

from save_form_database import SaveToDataBase


'''
  create the flask object and follow some rules
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here_a'
# define the Folder path here 

# app.config['UPLOAD_FOLDER'] = "static/uploads"

app.config["UPLOAD_WORKFLOW_FILES"]= "static/WORKFLOW_FILES"
ckeditor = CKEditor(app)
Bootstrap5(app)

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "nisers.db")}'
db.init_app(app)

# Define save_get_file_url function which take the the form file data , save the data in a given folder and returns path
def save_get_file_url(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_WORKFLOW_FILES'],filename)
    file.save(file_path)
    return file_path

TABLES = {
    'User Table': UserTable, 'DateTime Table': DateTimeTable, 'Station Table': StationTable, 
    'TempHumiDew Table': TempHumiDewTable, 'Material Receiver Common Table': MaterialReceivingCommonTable, 
    'Sensor Table': SensorTable, 'FEH Table': FEHTable, 'SEH Table': SEHTable, 'Main Bridge Table': MainBridgeTable, 
    'Stump Bridge Table': StumpBridgeTable, 'Kapton Tape Table': KaptonTapeTable, 'Other Table': OtherTable, 
    'VTRx Table': VTRxTable, 'Ground Balancer Table': GroundBalancerTable, 'Glue Table': GlueTable, 
    'Wire Bonder Table': WireBonderTable, 'Jig Table': JigTable, 'VSensor Table': VSensorTable, 
    'VFEH Table': VFEHTable, 'VSEH Table': VSEHTable, 'VMain Bridge Table': VMainBridgeTable, 
    'VStump Bridge Table': VStumpBridgeTable, 'Kapton Gluing Table': KaptonGluingTable, 
    'HV Table': HVTable, 'IV Table': IVTable, 'Sensor Gluing Table': SensorGluingTable, 
    'Needle Metrology Table': NeedleMetrologyTable, 'Skeleton Test Table': SkeletonTestTable, 
    'Hybrid Gluing Table': HybridGluingTable, 'Module Encapsulation Table': ModuleEncapsulationTable, 
    'Wire Bonding Table': WireBondingTable, 'Noise Test Ph2 ACF Table': NoiseTestPh2ACFTable, 
    'Noise Test GIPHT Table': NoiseTestGIPHTTable, 'Burn-in Test Table': BurninTestTable
}

FORM_MAPPING_VISUAL_INSPECTION = {
   "sensor_visual": [SensorVisualForm,"sensor_id",SensorTable,VSensorTable],
    "FEH_visual": [FEHVisualForm,"feh_id",FEHTable,VFEHTable],
    "SEH_visual": [SEHVisualForm,"seh_id",SEHTable,VSEHTable],
    "main_bridge_visual": [MainBridgeVisualForm,"main_bridge_id",MainBridgeTable,VMainBridgeTable],
    "stump_bridge_visual": [StumpBridgeVisualForm,"stump_bridge_id",StumpBridgeTable,VStumpBridgeTable]
}

    

#Flask log-in  ,this part is crucial for authenticaton 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return db.get_or_404(UserTable ,username)

#upload folder for the images
# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        result = db.session.execute(db.select(UserTable).where(UserTable.username == username))
        user = result.scalar()
        # Check if user exists and is active
        if not user:
            new_user_data = {
                "username": "john_doe",
                "password": "securepassword123",
                "name": "John Doe",
                "is_active": True
            }
            new_user = save_user_to_db(new_user_data)
            login_user(new_user)
            return redirect(url_for('secrets'))
        else :
            login_user(user) # ---------------------- work on this if it works -----
            return redirect(url_for('secrets'))
        # if user:
        #     if not user.is_active:
        #         flash("Your account is inactive. Please contact support.")
        #         return redirect(url_for('login'))
            
        #     # Verify password
        #     if user.password == password:
        #         login_user(user)
        #         return redirect(url_for('secrets'))
        #     else:
        #         flash("Incorrect password, please try again.")
        # else:
        #     flash("User does not exist, please check your email.")
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
# @app.route('/modules')
# @login_required
# def show_module():
#     data = db.session.query(HvIvFormTable).all()  # Assuming Station is the model
#     columns = HvIvFormTable.__table__.columns
#     return render_template("show_table.html", table_data=data, columns=columns)
#     return render_template("modules.html")
@app.route('/modules')
@login_required
def show_module():
    return render_template("modules.html")
# TABLES = {'Users': UserTable, "material_receiver" : MaterialReceivingCommonTable}
@app.route("/show_database_table", methods=["GET", "POST"])
def show_database_table():
    selected_table = request.form.get("table_name", "Users")  
    model = TABLES.get(selected_table, UserTable) 
    columns = [column.name for column in model.__table__.columns]
    rows = model.query.all()
    rows_data = [{column: getattr(row, column) for column in columns} for row in rows]
    return render_template("show_db_table.html", tables=TABLES.keys(), selected_table=selected_table, columns=columns, rows=rows_data)

def process_data(data):
    tables = {}
    if not data:
        return tables

    for entry in data:
        category = entry.get("material_type", "Unknown")  # Categorize by material_type
        if category not in tables:
            tables[category] = {"headers": entry.keys(), "rows": []}
        tables[category]["rows"].append(entry)

    return tables
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
    with app.app_context():
        result = db.session.execute(db.select(StationTable).order_by(StationTable.id))
        all_stations = result.scalars().all()
        return render_template("all_stations.html",all_stations = all_stations,user_name = current_user.username)
   
'''
This show_form functions adds the new station to the database and redirect to the the method stations page after successfull completion 

'''
@app.route("/station_form" ,methods=["GET","POST"])
@login_required
def show_form():
    form = AddStationForm()
    if form.validate_on_submit():
        time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        img_name = f"station_img{time_stamp}.png"
        form_data_dict = get_add_station_form_data(form,img_name)
        print(form_data_dict)
        save_station_to_db(form_data_dict)
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
    workflow_name = request.args.get('workflow_name', 'Workflow')
    if workflow_name=="Material Receiver" :
        if request.method == "POST":
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_name = f"material_receiver_{request.form.getlist('material_type[]')[0]}_{time_stamp}"
            form_data_dict = material_receiver_form_dict(request.form, file_name)
            print("form data dict", form_data_dict)
            save_material_receiving_data_to_db(form_data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(form_data_dict) + "\n") 
            return redirect(url_for('work_flow'))
        else:
            return render_template("material_reciever.html",select_material="Jig",station_names = get_station_info())
    elif workflow_name == "Visual Inspection":
        datetime_data ='2025-02-07'
        record_id = save_datetime_to_db(datetime_data)
        print(record_id)
        temp_humi_dew_data = {
    "temperature": 22.5,
    "dew_point": 15.3,
    "humidity": 65.4
}
        new_temp_humi_dew_record_id = save_temp_humi_dew_to_db(temp_humi_dew_data)
        print(new_temp_humi_dew_record_id)
        return render_template("visual_type.html")

    elif workflow_name == "Kapton Gluing":
        form = KaptonGluing()
        form.sensor_id.choices = get_field_values_with_id(SensorTable, "sensor_id")
        form.part_A_batch_no.choices = get_field_values_with_id(GlueTable,"glue_batch_id")
        form.part_B_batch_no.choices =  get_field_values_with_id(GlueTable,"glue_batch_id")
        form.jig_id.choices = get_field_values_with_id(JigTable,"name")
        form.station.choices = get_station_info()
        if is_choise_empty(workflow_name,form):
            workflow_name=="Material Receiver"
            return redirect(url_for('add_data',workflow_name="Material Receiver"))

        #add_choise_not_go_add_material(workflow_name)
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            filename = f"kapton_glue{time_stamp}.png"
            data_dict = get_dict_kapton_gluing_form(form,filename)
            print(data_dict)
            save_kapton_data(data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(data_dict) + "\n") 
            #SaveToDataBase().save_kapton_gluing_form(form,db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Hv Form":
        form = HvForm()
        sensor_type_ids = [(sensor[0],f"{sensor[1]} ({sensor[2]})") for sensor in get_field_values_with_id(SensorTable, "sensor_id","sensor_type") if sensor[2]]
        form.sensor_id.choices = sensor_type_ids
        form.station.choices = get_station_info()
        # form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            hv_csv_file_name = f"hv_csv{time_stamp}.csv"
            other_file_name =f"hv_other{time_stamp}.csv"
            dict_hv_data = get_dict_hv_form(form,hv_csv_file_name,other_file_name)
            print(dict_hv_data)
            save_hv_data(dict_hv_data)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(dict_hv_data) + "\n") 
            #SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Iv Form":
        
        form = IvForm()
        
        form.sensor_id.choices = get_field_values_with_id(SensorTable, "sensor_id","sensor_type")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            iv_csv_file_name = f"iv_csv{time_stamp}.csv"
            other_file_name = f"iv_other{time_stamp}.png"
            dict_iv_data = get_dict_iv_form(form,iv_csv_file_name,other_file_name)
            save_iv_data(dict_iv_data)
            print("iv test data ",dict_iv_data)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(dict_iv_data) + "\n") 
            #SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Sensor Gluing":
        form = SensorGluing()
        form.part_A_batch_no.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.part_B_batch_no.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.jig_id.choices = get_field_values_with_id(JigTable, "name")
        form.top_sensor_id.choices = sensor_type_ids = [(sensor[0],f"{sensor[1]} ({sensor[2]})") for sensor in get_field_values_with_id(SensorTable, "sensor_id","sensor_type") 
                                                        if sensor[2]=="Top Sensor"]
        form.bottom_sensor_id.choices = sensor_type_ids = [(sensor[0],f"{sensor[1]} ({sensor[2]})") for sensor in get_field_values_with_id(SensorTable, "sensor_id","sensor_type") 
                                                        if sensor[2]=="Bottom Sensor"]
        form.main_bridge_id.choices = get_field_values_with_id(MainBridgeTable, "main_bridge_id")
        form.stump_bridge_id.choices = get_field_values_with_id(StumpBridgeTable, "stump_bridge_id")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            image_name = f"sensor_gluing_img_{time_stamp}.png"
            dict_sensor_gluing_data = get_dict_sensor_gluing_form(form,image_name)
            print(dict_sensor_gluing_data)
            save_sens_gluing(dict_sensor_gluing_data)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(dict_sensor_gluing_data) + "\n") 
            #SaveToDataBase().save_sensor_gluing_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name =="Needle Metrology":
        form = NeedleMetrologyForm()
        form.bare_module_id.choices = get_field_values_with_id(SensorGluingTable, "bare_module_id")
        form.station.choices = get_station_info()
        # form.bare_module_id.choices = [(bare_module.bare_module_id, bare_module.bare_module_id) for bare_module in bare_module_ids]
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            csv_excel_file = f"Needle_csv_excel_{time_stamp}.png"
            image_file = f"image_file_{time_stamp}.png"
            data_needle_form = get_dict_needle_metrology(form,csv_excel_file,image_file)
            print(data_needle_form)
            save_needle_data(data_needle_form)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(data_needle_form) + "\n") 
            #SaveToDataBase().save_needle_metrology_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Skeleton Test":
        form = SkeletonTestForm()
        form.FEH_L.choices = get_field_values_with_id(FEHTable, "feh_id")
        form.FEH_R.choices = get_field_values_with_id(FEHTable, "feh_id")
        form.SEH.choices = get_field_values_with_id(SEHTable, "seh_id")
        form.VTRx.choices = get_field_values_with_id(VTRxTable, "vt_rx_id")
        form.ground_balancer_id.choices = get_field_values_with_id(GroundBalancerTable, "ground_balancer_id")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_name = f"skeleton_{time_stamp}.png"
            skeleton_dict = get_skeleton_test_form_data(form,file_name)
            print(skeleton_dict)
            save_skeleton_data(skeleton_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(skeleton_dict) + "\n") 
            #SaveToDataBase().save_skeleton_test_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Hybrid Gluing":
        form = HybridGluingForm()
        form.bare_module_id.choices = get_field_values_with_id(SensorGluingTable,"bare_module_id")
        form.skeleton_id.choices = get_field_values_with_id(SkeletonTestTable,"skeleton_id")
        form.part_A_batch_no.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.part_B_batch_no.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            image_name = f"hybrid_gluing_{time_stamp}.png"
            hybrid_data_dict = get_hybrid_gluing_form_data(form,image_name)
            print(hybrid_data_dict)
            save_hybrid_gluing_data(hybrid_data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(hybrid_data_dict) + "\n") 
            #SaveToDataBase().save_hybrid_gluing_form( form ,db ,app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif workflow_name == "Module Encapsulation":
        form = ModuleEncapsulationForm()
        form.module_id.choices = get_field_values_with_id(HybridGluingTable,"module_id")
        form.glue_a.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.glue_b.choices = get_field_values_with_id(GlueTable, "glue_batch_id")
        form.jig.choices = get_field_values_with_id(JigTable,"name")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            image_name = f"module_enmcapsualtion_{time_stamp}.png"
            module_encapsulation_data_dict = get_module_encapsulation_form_data(form,image_name)
            save_module_encapsulation_data(module_encapsulation_data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(module_encapsulation_data_dict) + "\n") 
            print(module_encapsulation_data_dict)
            return redirect(url_for('work_flow'))

    elif workflow_name == "Wire Bonding": 
        if request.method == 'POST':
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            img_name = f"wire_bonding_img_{time_stamp}.png"
            csv_name = f"wire_bonding_data_{time_stamp}.csv"
            wire_data_dict = wire_form_dict(request.form ,img_name , csv_name)
            print(wire_data_dict)
            save_wire_bonding_data(wire_data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(wire_data_dict) + "\n") 
            return redirect(url_for('work_flow'))
        form = WireBondingForm()
        return render_template('wire_bonding.html', form=form,module_ids =get_field_values_with_id(HybridGluingTable,"module_id"),station_names = get_station_info())
        
    elif workflow_name =="Noise Test Ph2-ACF":
        form = NoiseTestForm_Ph2_ACF()
        form.module_id.choices = get_field_values_with_id(HybridGluingTable,"module_id")
        form.station.choices = get_station_info()
        #form.module_id.choices = [(module.module_id, module.module_id) for module in module_ids]
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_dict = {
    "aldrino_file": f"aldrino{time_stamp}.yml",
    "hv_file": f"hvfile{time_stamp}.png",
    "lv_file": f"lvfile{time_stamp}.csv",
    "iv_file": f"ivfile{time_stamp}.txt",
    "root_file": f"data{time_stamp}.root"
}
            dict_data = get_noise_test_Ph2_ACF_form_data(form,file_dict)
            print(dict_data)
            save_noise_ph2ACF_data(dict_data)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(dict_data) + "\n") 
            return redirect(url_for('work_flow'))
    elif workflow_name == "Noise Test GIPHT":
        form = NoiseTestForm_GIPHT()
        form.module_id.choices = get_field_values_with_id(HybridGluingTable,"module_id")
        form.station.choices = get_station_info()
        if form.validate_on_submit():
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_dict = {
    "aldrino_file": f"aldrino{time_stamp}.yml",
    "hv_file": f"hvfile{time_stamp}.png",
    "lv_file": f"lvfile{time_stamp}.csv",
    "iv_file": f"ivfile{time_stamp}.txt",
    "root_file": f"data{time_stamp}.root"
}
            data_dict = get_noise_test_GIPHT_form_data(form,file_dict)
            save_noise_GIPHT_data(data_dict)
            print(data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(data_dict) + "\n") 
            return redirect(url_for('work_flow'))
    elif workflow_name == "Burnin Test":
        if request.method =="POST":
            time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_dict = {
    "tracker_root_file": f"tracker_root_{time_stamp}.root",
    "tracker_monitor_root_file": f"tracker_monitor_{time_stamp}.root",
    "press_supply_root_file": f"press_supply_{time_stamp}.root",
    "burnnin_box_root_file": f"burnin_box_{time_stamp}.root"
}
            data_dict   = burnin_form_dict(request.form, file_dict)
            save_burnin_test_data(data_dict)
            print(data_dict)
            with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(data_dict) + "\n") 
            return redirect(url_for('work_flow'))
        return render_template("BurninTest.html",module_ids =get_field_values_with_id(HybridGluingTable,"module_id"),station_names=get_station_info())
    return render_template("visual_inspection.html", form=form, process_name=workflow_name)




def get_dict_form_visual(form,file_name,material_type):
    # dict_materials = {'sensor_visual':"sensor_id",'FEH_visual':"feh_id",'SEH_visual':"seh_id",'main_bridge_visual':"main_bridge_id",
    #                   'stump_bridge_visual':"stump_bridge_id"}
    form_data_dict = {
            "material_type":material_type, 
            "material_id": int(form.material_id.data),
            "station": int(form.station.data),
            "temp": form.temp.data,
            "humidity": form.humidity.data,
            "dew_point": form.dew_point.data,
            "working_date": form.working_date.data.strftime('%Y-%m-%d'),
            "image_url": save_get_file_url(form.image.data,file_name),  # Save file and get the URL
            "comment": form.comment.data
        }
    print(type(form_data_dict["material_id"]))
    return form_data_dict
# < ---------------------- Visual Inspection Part ------------------------------
@app.route('/visual_inspection_data', methods=["GET", "POST"])
def visual_inspection_data():
    material_type = request.args.get("material_type")
    material_list = FORM_MAPPING_VISUAL_INSPECTION[material_type]
    visual_material_form = material_list[0]()
    visual_material_form.station.choices = get_station_info()
    visual_material_form.material_id.choices = get_field_values_with_id(material_list[2], material_list[1])
    if visual_material_form.validate_on_submit():
        time_stamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        file_name = f"visual_{material_type}_{time_stamp}.png"
        form_dict_data = get_dict_form_visual(visual_material_form,file_name,material_type)
        print(form_dict_data)
        print(save_datetime_to_db(form_dict_data["working_date"]))
        save_visual_data_to_db(form_dict_data,material_list)
        with open("form_data.jsonl", "a") as f:
                f.write(json.dumps(form_dict_data) + "\n") 
        return redirect(url_for('work_flow'))
    return render_template("visual_inspection.html",form = visual_material_form)

def get_station_info():
    stations = db.session.query(StationTable.id, StationTable.station_name).all()
    formatted_stations = [(station_id,station_name) for station_id, station_name in stations]
    return formatted_stations
def get_field_values_with_id(model, *field_names):
    try:
        # Get the primary key field name dynamically
        primary_key = inspect(model).primary_key[0].name  
        
        # Ensure all requested fields exist in the model
        fields = [getattr(model, field_name) for field_name in field_names]
        
        # Query the database for the primary key and requested fields
        query_results = db.session.query(getattr(model, primary_key), *fields).all()
        
        return [tuple(record) for record in query_results]
    
    except AttributeError as e:
        raise ValueError(f"One or more fields do not exist in {model.__name__}: {e}")

def is_choise_empty(workflow_name: str, form: object) -> bool:
    workflows_choices = {
"Visual Inspection": [
    "sensor_id", "feh_id", "seh_id", "main_bridge_id", "stump_bridge_id"
],
"Kapton Gluing": [
    "sensor_id", "part_A_batch_no", "part_B_batch_no", 
    "jig_id", "station"
],
"Hv Form": [
    "sensor_id", "station"
],
"Iv Form": [
    "sensor_id", "station"
],
"Sensor Gluing": [
    "part_A_batch_no", "part_B_batch_no", "jig_id", 
    "top_sensor_id", "bottom_sensor_id", "main_bridge_id", 
    "stump_bridge_id", "station"
],
"Needle Metrology": [
    "bare_module_id", "station"
],
"Skeleton Test": [
    "FEH_L", "FEH_R", "SEH", "VTRx", 
    "ground_balancer_id", "station"
],
"Hybrid Gluing": [
    "bare_module_id", "skeleton_id", 
    "part_A_batch_no", "part_B_batch_no", "station"
],
"Module Encapsulation": [
    "module_id", "glue_a", "glue_b", 
    "jig", "station"
],
"Wire Bonding": [
    "module_ids", "station_names"
],
"Noise Test Ph2-ACF": [
    "module_id", "station"
],
"Noise Test GIPHT": [
    "module_id", "station"
],
"Burnin Test": [
    "module_ids", "station_names"
]
}
    required_fields = workflows_choices.get(workflow_name)

    if required_fields is None:
        return True 

    if isinstance(required_fields, dict):
        for field in required_fields:
            if hasattr(form, field) and getattr(form, field).choices == []:
                return True  

    if isinstance(required_fields, list):
        for field in required_fields:
            if hasattr(form, field) and getattr(form, field).choices == []:
                return True 

    return False 
def save_get_file_url(file,file_name):
    file_name = secure_filename(file_name)
    try:
        file_path = os.path.join(app.config['UPLOAD_WORKFLOW_FILES'],file_name)
        file.save(file_path)
        return file_name
    except:
        print("Failed to save the file")
        return None
def get_add_station_form_data(form,img_name):
    return {
        "station_name": form.station_name.data,
        "station_img": save_get_file_url(form.station_img.data,img_name),  # Station Image upload
        "station_remarks": form.station_remarks.data,
        "station_created_at": form.station_created_at.data.strftime('%Y-%m-%d %H:%M:%S') if form.station_created_at.data else None,
        "station_location": form.station_location.data,
        "station_is_active": form.station_is_active.data,  # Boolean field
        "station_operator": form.station_operator.data,
        "station_iteration_number": form.station_iteration_number.data
    }

def material_receiver_form_dict(form ,filename):
    materials = {"material_type":None,"common_data":None,"material_data":None}
    materials["common_data"] = {"received_from":form.get('received_from', 'Unknown'),"date":form.get('date', 'Unknown'),
                                "temperature":form.get('temperature', 'Unknown'),"humidity":form.get('humidity', 'Unknown'), "dew_point":form.get('dew_point', 'Unknown'),"station_id":int(form.get('station_name', 'Unknown')),
                                "material_comment":form.get('material_comment', ''),"img_url":None}
    material_data = {"Sensor":None,"FEH":None,"SEH":None,"Main Bridge":None ,"Stump Bridge":None,"Glue":None,"Kapton Tapes":None,
                     "Optical Fibre":None ,"Wire Bonder":None , "Other":[]}
    for file_key in request.files:
            file = request.files[file_key]
            if file.filename:
                # filename = "filename"
                file_name = save_get_file_url(file,filename)
                materials["common_data"]["img_url"]=file_name
            else:
                print(f"Empty file upload: {file_key}")
    materials["material_type"]=form.getlist('material_type[]')[0]
    if form.getlist('material_type[]')[0]=="Glue":
        materials["material_data"]={"material_ids":form.getlist('material_id[]'),"expiry_dates":form.getlist('expiry_date[]')}

    elif form.getlist('material_type[]')[0]=="Wire Bonder":
        materials["material_data"]={"material_ids":form.getlist('material_id[]'),"expiry_dates":form.getlist('expiry_date[]'),"spool_numbers": form.getlist('spool_number[]') ,
                                    "wedge_tool_numbers":form.getlist('wedge_tool_no[]')}
    else :
        print("else")
        materials["material_data"]={"material_ids":form.getlist('material_id[]')}
    return materials

def get_dict_kapton_gluing_form(form,filename):       
    data_dict = {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d'),
        "sensor_id": form.sensor_id.data,
        "sensor_type": form.sensor_type.data,
        "cooling_points": form.cooling_points.data,
        "part_A_batch_no": form.part_A_batch_no.data,
        "part_B_batch_no": form.part_B_batch_no.data,
        "jig_no": form.jig_id.data,
        "station_id":int(form.station.data),
        "image": save_get_file_url(form.image.data,filename),
        "comment": form.comment.data
    }
    print(data_dict["station_id"])
    return data_dict
            
def get_dict_hv_form(form,hv_csv_file_name,other_file_name):
    data_dict = {
"temp": form.temp.data,
"humidity": form.humidity.data,
"dew_point": form.dew_point.data,
"working_date": form.working_date.data.strftime('%Y-%m-%d'),
"sensor_id": form.sensor_id.data,
"station_id":int(form.station.data),
"cooling_points": form.cooling_points.data,
"hv_csv": save_get_file_url(form.hv_csv.data,hv_csv_file_name),  # CSV file upload
"image": save_get_file_url(form.image.data,other_file_name),  # Optional image upload
"comment": form.comment.data,
}
    return data_dict
def get_dict_iv_form(form,iv_csv_file_name,other_file_name):
    data_dict = {
"temp": form.temp.data,
"humidity": form.humidity.data,
"dew_point": form.dew_point.data,
"working_date": form.working_date.data.strftime('%Y-%m-%d'),
"sensor_id": form.sensor_id.data,
"station_id":int(form.station.data),
"cooling_points": form.cooling_points.data,
"iv_csv": save_get_file_url(form.iv_csv.data,iv_csv_file_name),  # CSV file upload
"image": save_get_file_url(form.image.data,other_file_name),  # Optional image upload
"comment": form.comment.data,
}
    return data_dict
def get_dict_sensor_gluing_form(form,image_file):
    data_dict = {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "bare_module_id": form.bare_module_id.data,
        "top_sensor_id": form.top_sensor_id.data,
        "bottom_sensor_id": form.bottom_sensor_id.data,
        "main_bridge_id": form.main_bridge_id.data,
        "stump_bridge_id": form.stump_bridge_id.data,
        "module_spacing": form.module_spacing.data,
        "cooling_points": form.cooling_points.data,
        "jig_id": form.jig_id.data,
        "station_id":int(form.station.data),
        "part_A_batch_no": form.part_A_batch_no.data,
        "part_B_batch_no": form.part_B_batch_no.data,
        "image":save_get_file_url(form.image.data,image_file),
        "comment": form.comment.data,
    }
    return data_dict
def get_dict_needle_metrology(form,csv_excel_file,image_file):
    data_dict ={
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "bare_module_id": form.bare_module_id.data,
        "station_id":int(form.station.data),
        "x_coordinate": form.x_coordinate.data,
        "y_coordinate": form.y_coordinate.data,
        "del_theta": form.del_theta.data,
        "csv_excel": save_get_file_url(form.csv_excel.data,csv_excel_file),  
        "image": save_get_file_url(form.image.data,image_file),  
        "comment": form.comment.data
    }
    return data_dict
def get_skeleton_test_form_data(form,file_name):
    return {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "skeleton_id": form.skeleton_id.data,
        "FEH_L": form.FEH_L.data,
        "FEH_R": form.FEH_R.data,
        "SEH": form.SEH.data,
        "VTRx": form.VTRx.data,
        "ground_balancer_id": form.ground_balancer_id.data,
        "station_id":int(form.station.data),
        "file": save_get_file_url(form.file.data,file_name), 
        "comment": form.comment.data
    }
def get_hybrid_gluing_form_data(form,image_name):
    return {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "module_id": form.module_id.data,
        "bare_module_id": form.bare_module_id.data,
        "skeleton_id": form.skeleton_id.data,
        "part_A_batch_no": form.part_A_batch_no.data,
        "part_B_batch_no": form.part_B_batch_no.data,
        "station_id":int(form.station.data),
        "image": save_get_file_url(form.image.data,image_name),  # Optional image upload
        "comment": form.comment.data,
    }
def get_module_encapsulation_form_data(form,image_name):
    return {
        "temp":form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "module_id": form.module_id.data,
        "glue_a": form.glue_a.data,
        "glue_b": form.glue_b.data,
        "glue_preparation_time": form.glue_preparation_time.data,
        "jig": form.jig.data,
        "station": form.station.data,
        "comment": form.comment.data,
        "img":save_get_file_url(form.img.data,image_name) ,  
    }

def get_noise_test_Ph2_ACF_form_data(form,file_dict):
    return {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "module_id": form.module_id.data,
        "station_id":int(form.station.data),
        "aldrino_file": save_get_file_url(form.upload_folder1.data,file_dict["aldrino_file"]),  # Aldrino File
        "hv_file": save_get_file_url(form.upload_folder2.data,file_dict["hv_file"]),  # HV File
        "lv_file": save_get_file_url(form.upload_folder3.data,file_dict["lv_file"] ),
        "iv_file": save_get_file_url(form.upload_folder4.data,file_dict["iv_file"]),  # IV File

        "root_file": save_get_file_url(form.upload_folder5.data,file_dict["root_file"]),  # ROOT File
        "comment": form.comment.data,
    }
def get_noise_test_GIPHT_form_data(form,file_dict):
    return {
        "temp": form.temp.data,
        "humidity": form.humidity.data,
        "dew_point": form.dew_point.data,
        "working_date": form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None,
        "module_id": form.module_id.data,
        "station_id":int(form.station.data),
        "aldrino_file": save_get_file_url(form.upload_folder1.data,file_dict["aldrino_file"]),  # Aldrino File
        "hv_file": save_get_file_url(form.upload_folder2.data,file_dict["hv_file"]),  # HV File
        "lv_file": save_get_file_url(form.upload_folder3.data,file_dict["lv_file"] ),
        "iv_file": save_get_file_url(form.upload_folder4.data,file_dict["iv_file"]),  # IV File
        "root_file": save_get_file_url(form.upload_folder5.data,file_dict["root_file"]),  # ROOT File
        "comment": form.comment.data,
    }
def wire_form_dict(form ,img_name , csv_name):
    data_dict = {"module_id":form.get('module_id'),"station_name":form.get("station_name"),"temparature":form.get('temperature'),"dewpoint":form.get('dewpoint'),"humidity":form.get('humidity'),"working_date":form.get('date', 'Unknown'),
                 "comment":form.get('comment'),"img_url":None,"top_parameter":None, "bottom_parameter":None , "csv_file":None
                 }
    # data_dict["working_date"]=form.working_date.data.strftime('%Y-%m-%d') if form.working_date.data else None
    if 'image' in request.files:
            image = request.files['image']
            if image :
                data_dict["img_url"]=save_get_file_url(image,img_name)
    def process_parameters(prefix):
            return {
                'delta_height': request.form.get(f'{prefix}_delta_height'),
                'correction_factor_k1': request.form.get(f'{prefix}_correction_factor_k1'),
                'correction_factor_k2': request.form.get(f'{prefix}_correction_factor_k2'),
                'mean_force_1': request.form.get(f'{prefix}_mean_force_1'),
                'mean_force_2': request.form.get(f'{prefix}_mean_force_2'),
                'rms_value': request.form.get(f'{prefix}_rms_value'),
                'standard_deviation': request.form.get(f'{prefix}_standard_deviation')
            }
    data_dict["top_parameter"] =  process_parameters('top')
    data_dict["bottom_parameter"] = process_parameters('bottom')
    def process_table_data(prefix):
            data = []
            i = 1
            while True:
                if not request.form.get(f'{prefix}_raw_pull_force_{i}'):
                    break
                
                row_data = {
                    'sensor_type': prefix,  # Adding sensor type
                    'raw_pull_force': request.form.get(f'{prefix}_raw_pull_force_{i}'),
                    'distance_between_feet': request.form.get(f'{prefix}_distance_between_feet_{i}'),
                    'type_of_break': request.form.get(f'{prefix}_type_of_break_{i}'),
                    'correction_factor': request.form.get(f'{prefix}_correction_factor_{i}'),
                    'corrected_force': request.form.get(f'{prefix}_corrected_force_{i}')
                    
                }
                data.append(row_data)
                print(f"\n{prefix.capitalize()} Row {i}:")
                print(json.dumps(row_data, indent=2))
                i += 1
            return data

    def generate_csv(file_name):
        top_data = process_table_data('top')
        bottom_data = process_table_data('bottom')
        combined_data = top_data + bottom_data
        csv_file =os.path.join(app.config['UPLOAD_WORKFLOW_FILES'],file_name)
        try:
            with open(csv_file, mode='w', newline='') as file:
                fieldnames = ['sensor_type', 'raw_pull_force', 'distance_between_feet', 'type_of_break', 'correction_factor', 'corrected_force', 'comment']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(combined_data)
            return file_name 
        except:
            return None
    data_dict["csv_file"]=generate_csv(csv_name)  
    return data_dict  
def burnin_form_dict(form, file_dict):
                data_dict = {
                    "temperature": form.get('temperature'),
                    "humidity": form.get('humidity'),
                    "dewPoint": form.get('dewPoint'),
                    "workingDate": form.get('workingDate'),
                    "station_name":form.get("station_name"),
                    "module_id": form.getlist('module_id_left[]')+form.getlist('module_id_right[]'),
                     
                    "comment": form.get('comments'),
                    "tracker_root_file": None,
                    "tracker_monitor_root_file": None,
                    "press_supply_root_file":None,
                    "burnnin_box_root_file":None
                }
                
                if 'Tracker ROOT File' in request.files:
                    tracker_root = request.files['Tracker ROOT File']
                    if tracker_root:
                        data_dict["tracker_root_file"] = save_get_file_url(tracker_root, file_dict["tracker_root_file"])

                if 'Tracker Monitor ROOT File' in request.files:
                    tracker_monitor_file = request.files['Tracker Monitor ROOT File']
                    if tracker_monitor_file:
                        data_dict["tracker_monitor_root_file"] = save_get_file_url(tracker_monitor_file,file_dict["tracker_monitor_root_file"] )
                if 'Press Supply ROOT File' in request.files:
                    press_supply_file = request.files['Press Supply ROOT File']
                    if press_supply_file:
                        data_dict["press_supply_root_file"] = save_get_file_url(press_supply_file, file_dict["press_supply_root_file"])

                if "Press Supply ROOT File" in request.files:
                    burnin_box_file = request.files['Press Supply ROOT File']
                    if burnin_box_file:
                        data_dict["burnnin_box_root_file"] = save_get_file_url(burnin_box_file, file_dict["burnnin_box_root_file"])

                return data_dict     


def save_user_to_db(user_data: dict):
    valid_fields = {column.name for column in UserTable.__table__.columns}
    filtered_data = {k: v for k, v in user_data.items() if k in valid_fields}
    
    user = UserTable(**filtered_data)
    
    try:
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e
def save_datetime_to_db(working_date):
    working_date_value = working_date
    if not working_date_value:
        raise ValueError("The 'working_date' field is required.")
    try:
        if isinstance(working_date_value, str):
            working_date_value = datetime.datetime.strptime(working_date_value, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("The 'working_date' must be in 'YYYY-MM-DD' format.")
    new_record = DateTimeTable(working_date=working_date_value)
    try:
        db.session.add(new_record)
        db.session.commit()
        return new_record.id
    except Exception as e:
        db.session.rollback()
        raise e
def save_temp_humi_dew_to_db(temp_humi_dew_data: dict):
    valid_fields = {column.name for column in TempHumiDewTable.__table__.columns}
    filtered_data = {k: v for k, v in temp_humi_dew_data.items() if k in valid_fields}
    
    temp_humi_dew_record = TempHumiDewTable(**filtered_data)
    
    try:
        db.session.add(temp_humi_dew_record)
        db.session.commit()
        return temp_humi_dew_record.id
    except Exception as e:
        db.session.rollback()
        raise e
def get_current_user_id():
    if current_user.is_authenticated:
        return current_user.id
    else:
        return None  # Or raise an exception if preferred
def save_visual_data_to_db(form_dict, material_list):
    visual_data = {
        "image": form_dict.get("image_url", None),
        "comment": form_dict.get("comment", ""),
        "datetime_id":save_datetime_to_db(form_dict.get("working_date")),
        "user_id": get_current_user_id(),
        material_list[1]: form_dict.get("material_id"),
        "station_id": form_dict.get("station"),
        "temp_humi_dewid": save_temp_humi_dew_to_db({
            "temperature": form_dict.get("temp", 0.0),
            "dew_point": form_dict.get("dew_point", 0.0),
            "humidity": form_dict.get("humidity", 0.0)
        })
    }
    print(visual_data["temp_humi_dewid"])
    print(save_datetime_to_db(form_dict.get("working_date")))
    valid_fields = {column.name for column in material_list[3].__table__.columns}
    print(valid_fields)
    if material_list[1] not in valid_fields:
        raise ValueError(f"Invalid field name '{material_list[1]}' for table {material_list[3].__name__}")
    filtered_data = {k: v for k, v in visual_data.items() if k in valid_fields}
    visual_record = material_list[3](**filtered_data)

    try:
        db.session.add(visual_record)
        db.session.commit()
        return visual_record
    except Exception as e:
        db.session.rollback()
        raise e
from sqlalchemy.exc import SQLAlchemyError

def save_kapton_data(data_dict):
    datetime_id = save_datetime_to_db(data_dict.get("working_date")) 
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    user_id = get_current_user_id() 
    kapton_record = KaptonGluingTable(
    cooling_point=data_dict.get("cooling_points").replace(" ", ""),  # Fix space issue
    image=data_dict.get("image", None),
    comment=data_dict.get("comment", ""),
    glue_idA=int(data_dict.get("part_A_batch_no")),  # Convert to int
    glue_idB=int(data_dict.get("part_B_batch_no")),  # Convert to int
    date_time_id=datetime_id,  # Ensure this is correctly set
    user_id=user_id,  # Ensure this is correctly set
    temp_humi_dew_id=temp_humi_dew_id,  # Ensure this is correctly set
    sensor_id=int(data_dict.get("sensor_id")),  # Convert to int
    jig_id=int(data_dict.get("jig_no")),  # Convert to int
    station_id=int(data_dict.get("station_id"))  # Ensure correct type
)

    try:
        db.session.add(kapton_record)  
        db.session.commit()
        update_record(SensorTable,kapton_record.sensor_id,"sensor_type",data_dict.get("sensor_type"))  
        return kapton_record
    except Exception as e:
        db.session.rollback()
        raise e
def save_hv_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    hv_record = HVTable(
        cooling_point=data_dict.get("cooling_points").replace(" ", ""),  # Fix space issue
        hv_csv=data_dict.get("hv_csv", None),
        optional_file=data_dict.get("image", None),  # Mapping 'image' to 'optional_file'
        comment=data_dict.get("comment", ""),
        datetime_id=save_datetime_to_db(data_dict.get("working_date")),  
        user_id=get_current_user_id() ,  
          
        station_id=int(data_dict.get("station_id")),  
        temp_humi_dewid=temp_humi_dew_id  
    )

    db.session.add(hv_record) 
    db.session.commit() 
def save_iv_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    iv_record = IVTable(
        cooling_point=data_dict.get("cooling_points").replace(" ", ""),  
        iv_csv=data_dict.get("iv_csv", None),
        optional_file=data_dict.get("image", None), 
        comment=data_dict.get("comment", ""),
        datetime_id=save_datetime_to_db(data_dict.get("working_date")),  
        user_id=get_current_user_id() ,  
        sensor_id=int(data_dict.get("sensor_id")),  
        station_id=int(data_dict.get("station_id")),  
        temp_humi_dewid=temp_humi_dew_id  
    )

    db.session.add(iv_record) 
    db.session.commit()  
def save_sens_gluing(data_dict):
    module_spacing = float(data_dict.get("module_spacing").replace("mm", ""))
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    sensor_gluing_record = SensorGluingTable(
        bare_module_id=data_dict.get("bare_module_id"),
        module_spacing=module_spacing,
        cooling_point=data_dict.get("cooling_points").replace(" ", ""),  
        image=data_dict.get("image", None),
        comment=data_dict.get("comment", ""),
        bottom_sensor_id=int(data_dict.get("bottom_sensor_id")),  # Convert to int
        top_sensor_id=int(data_dict.get("top_sensor_id")),  # Convert to int
        mainbridgeid=int(data_dict.get("main_bridge_id")),  # Convert to int
        stumpbridge_id=int(data_dict.get("stump_bridge_id")),  # Convert to int
        jig_id=int(data_dict.get("jig_id")),  # Convert to int
        station_id=int(data_dict.get("station_id")),  # Convert to int
        glue_idA=int(data_dict.get("part_A_batch_no")),  # Convert to int
        glue_idB=int(data_dict.get("part_B_batch_no")),  # Convert to int
        datetimeid=save_datetime_to_db(data_dict.get("working_date")),  # Ensure this is correctly set
        user_id=get_current_user_id(),  # Ensure this is correctly set
        temp_humi_dewid=temp_humi_dew_id  # Ensure this is correctly set
    )

    db.session.add(sensor_gluing_record)  # Add record to session
    db.session.commit()  # Commit transaction
def save_needle_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    delta_x = float(data_dict.get("x_coordinate"))
    delta_y = float(data_dict.get("y_coordinate"))
    rotation = float(data_dict.get("del_theta"))

    needle_metrology_record = NeedleMetrologyTable(
        user_id=get_current_user_id(),  # Ensure this is correctly set
        delta_x=delta_x,
        delta_y=delta_y,
        rotation=rotation,
        data_file=data_dict.get("csv_excel", None),  # Store CSV/Excel file path
        image=data_dict.get("image", None),
        comment=data_dict.get("comment", ""),
        datetime_id=save_datetime_to_db(data_dict.get("working_date")),  # Ensure this is correctly set
        temp_humi_dew_id=temp_humi_dew_id,  # Ensure this is correctly set
        sensor_gluing_id=int(data_dict.get("bare_module_id")),  # Convert to int
        jig_id=1,  # Convert to int if available
        station_id=int(data_dict.get("station_id")),  # Convert to int
    )

    db.session.add(needle_metrology_record)  # Add to session
    db.session.commit()  # Commit transaction
def save_skeleton_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    skeleton_test_record = SkeletonTestTable( 
        skeleton_id=data_dict.get("skeleton_id"),
        upload_img=data_dict.get("file", None),  # Map file → upload_img
        comment=data_dict.get("comment", ""),
        feh_idL=int(data_dict.get("FEH_L")),
        feh_idR=int(data_dict.get("FEH_R")),
        seh_id=int(data_dict.get("SEH")),
        vtrxid=int(data_dict.get("VTRx")),
        groundebalancer_id=int(data_dict.get("ground_balancer_id")),
        station_id=int(data_dict.get('station_id')),
        jigid=1,
        datetimeid=save_datetime_to_db(data_dict.get("working_date")),  # Ensure this is correctly set
        temp_humi_id=temp_humi_dew_id,  # Ensure this is correctly set
        userid=get_current_user_id() # Ensure this is correctly set
    )
    update_record(FEHTable,int(data_dict.get("FEH_L")),"feh_type","LEFT")
    update_record(FEHTable,int(data_dict.get("FEH_R")),"feh_type","RIGHT")
    db.session.add(skeleton_test_record)  # Add to session
    db.session.commit()
def save_hybrid_gluing_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    hybrid_gluing_record = HybridGluingTable(
        upload_img=data_dict.get("image", None),  # Map image → upload_img
        comment=data_dict.get("comment", ""),
        module_id=data_dict.get("module_id"),  # If module_id should be bare_module_id
        sensorgluing_id=data_dict.get("bare_module_id"),
        skeletontest_id=data_dict.get("skeleton_id"),
        glue_idA=int(data_dict.get("part_A_batch_no", 0)),  # Convert to int
        glue_idB=int(data_dict.get("part_B_batch_no", 0)),  # Convert to int
        station_id=int(data_dict.get("station_id")),
        jig_id =1, # not included in forms 
        datetimeid=save_datetime_to_db(data_dict.get("working_date")),  # Ensure datetime_id is correctly set
        temp_humi_dew_id=temp_humi_dew_id,  # Ensure tempid is correctly set
        userid=get_current_user_id() # Ensure userid is correctly set
    )

    db.session.add(hybrid_gluing_record)  # Add to session
    db.session.commit()  # Commit transaction
def save_module_encapsulation_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })

    # Create a new database entry for Module Encapsulation
    module_encapsulation_record = ModuleEncapsulationTable(
        glue_idA=int(data_dict.get("glue_a")),  
        glue_idB=int(data_dict.get("glue_b")), 
        preparation_time = float(data_dict.get("glue_preparation_time", 0)),
        comment=data_dict.get("comment", ""),
        image=data_dict.get("img", None),  
        date_time_id=save_datetime_to_db(data_dict.get("working_date")),  
        user_id=get_current_user_id(),  
        temp_humi_dew_id=temp_humi_dew_id,  
        hybrid_gluing_id=int(data_dict['module_id']),  
        jig_id=int(data_dict.get("jig", 0)),
        station_id=int(data_dict.get("station", 0))
    )

    # Add to session and commit
    db.session.add(module_encapsulation_record)
    db.session.commit()  # Commit transaction
def save_wire_bonding_data(data_dict):
    # Save temperature, humidity, and dewpoint data
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temparature", 0.0),
        "dew_point": data_dict.get("dewpoint", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })

    date_time_id = save_datetime_to_db(data_dict.get("working_date"))

    # Create a new database entry for Wire Bonding
    wire_bonding_record = WireBondingTable(
        comment=data_dict.get("comment", ""),
        upload_img=data_dict.get("img_url", None),
        excel_file=data_dict.get("csv_file", None),
        
        # Delta heights
        delta_height_top=float(data_dict.get("top_parameter", {}).get("delta_height", 0.0)),
        delta_height_bottom=float(data_dict.get("bottom_parameter", {}).get("delta_height", 0.0)),

        # Correction factors
        correction_factor_K1_top=float(data_dict.get("top_parameter", {}).get("correction_factor_k1", 0.0)),
        correction_factor_K1_bottom=float(data_dict.get("bottom_parameter", {}).get("correction_factor_k1", 0.0)),

        correction_factor_K2_top=float(data_dict.get("top_parameter", {}).get("correction_factor_k2", 0.0)),
        correction_factor_K2_bottom=float(data_dict.get("bottom_parameter", {}).get("correction_factor_k2", 0.0)),

        # Mean force values
        mean_force_1_top=float(data_dict.get("top_parameter", {}).get("mean_force_1", 0.0)),
        mean_force_1_bottom=float(data_dict.get("bottom_parameter", {}).get("mean_force_1", 0.0)),
        mean_force_2_top=float(data_dict.get("top_parameter", {}).get("mean_force_2", 0.0)),
        mean_force_2_bottom=float(data_dict.get("bottom_parameter", {}).get("mean_force_2", 0.0)),

        # RMS values
        rms_value_top=float(data_dict.get("top_parameter", {}).get("rms_value", 0.0)),
        rms_value_bottom=float(data_dict.get("bottom_parameter", {}).get("rms_value", 0.0)),

        # Standard Deviation values
        std_deviation_top=float(data_dict.get("top_parameter", {}).get("standard_deviation", 0.0)),
        std_deviation_bottom=float(data_dict.get("bottom_parameter", {}).get("standard_deviation", 0.0)),

        # Relations to other tables
        date_time_id=date_time_id,
        userid=get_current_user_id(),  # Assuming a function to get current user ID
        temp_humi_dew_id=temp_humi_dew_id,
        hybrid_gluing_id=int(data_dict.get("module_id", 0)),
        jig_id=int(data_dict.get("jig", 0)),
        station_id=int(data_dict.get("station_name", 0))
    )

    
    db.session.add(wire_bonding_record)
    db.session.commit()  
def save_noise_ph2ACF_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    noise_test_ph2ACF_record = NoiseTestPh2ACFTable(
       aldrino_file=data_dict.get("aldrino_file", None),
        hv_file=data_dict.get("hv_file", None),
        lv_file=data_dict.get("lv_file", None),
        iv_file=data_dict.get("iv_file", None),
        root_file=data_dict.get("root_file", None),
        comment=data_dict.get("comment", ""),
        datetimeid=save_datetime_to_db(data_dict.get("working_date")),
        user_id=get_current_user_id(), 
        temp_id=temp_humi_dew_id,
        hybrid_gluing_id=int(data_dict.get("module_id", 0)),
        station_id=int(data_dict.get("station_id", 0))
    )
    db.session.add(noise_test_ph2ACF_record)
    db.session.commit()  
def save_noise_GIPHT_data(data_dict):
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": data_dict.get("temp", 0.0),
        "dew_point": data_dict.get("dew_point", 0.0),
        "humidity": data_dict.get("humidity", 0.0)
    })
    noise_test_GIPHIT_record = NoiseTestGIPHTTable(
       aldrino_file=data_dict.get("aldrino_file", None),
        hv_file=data_dict.get("hv_file", None),
        lv_file=data_dict.get("lv_file", None),
        iv_file=data_dict.get("iv_file", None),
        root_file=data_dict.get("root_file", None),
        comment=data_dict.get("comment", ""),
        datetimeid=save_datetime_to_db(data_dict.get("working_date")),
        user_id=get_current_user_id(), 
        temp_humi_dew_id=temp_humi_dew_id,
        hybrid_gluing_id=int(data_dict.get("module_id", 0)),
        station_id=int(data_dict.get("station_id", 0))
    )
    db.session.add(noise_test_GIPHIT_record)
    db.session.commit()  
def save_station_to_db(form_dict):
            station_data = {
    "station_name": form_dict["station_name"],
    "station_location": form_dict["station_location"],
    "remarks": form_dict["station_remarks"],
    "img_path": form_dict["station_img"],
    "iteration_number": form_dict["station_iteration_number"],
    "operator_id": get_current_user_id() # Example user ID
}
            valid_fields = {column.name for column in StationTable.__table__.columns}
            filtered_data = {k: v for k, v in station_data.items() if k in valid_fields}
            station_record = StationTable(**filtered_data)
            
            try:
                db.session.add(station_record)
                db.session.commit()
                return station_record
            except Exception as e:
                db.session.rollback()
                raise e

def save_material_receiving_data_to_db(form_data_dict):
    received_date_value = form_data_dict["common_data"].get("date")
    if received_date_value:
        try:
            received_date_value = datetime.datetime.strptime(received_date_value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("The 'received_date' must be in 'YYYY-MM-DD' format.")
    else:
        raise ValueError("The 'received_date' field is required.")
    '''
    {"material_type": "Sensor", "common_data": {"received_from": "sdf", "date": "2025-02-12", "temperature": "23", "humidity": "23", "dew_point": "23", "station_name": "station_4", "material_comment": "dsfr", "img_url": "material_receiver.png"}, "material_data": {"material_ids": ["3er", "43", "lregejth"]}}    '''   
    material_data = {
        "received_from": form_data_dict["common_data"]["received_from"],
        "received_date": received_date_value, 
        "material_name": form_data_dict["material_type"],
        "img": form_data_dict["common_data"]["img_url"],
        "comment": form_data_dict["common_data"]["material_comment"],
        "user_id": get_current_user_id(),  
        "datetime_id": save_datetime_to_db(form_data_dict["common_data"]["date"]), 
        "temp_humi_dew_id": save_temp_humi_dew_to_db({"temperature":form_data_dict["common_data"]["temperature"],"dew_point":form_data_dict["common_data"]["dew_point"],"humidity":form_data_dict["common_data"][ "humidity"]}), 
        "station_id": form_data_dict["common_data"]["station_id"]  
    }
    print(material_data)
    valid_fields = {column.name for column in MaterialReceivingCommonTable.__table__.columns}
    filtered_data = {k: v for k, v in material_data.items() if k in valid_fields}
    material_record = MaterialReceivingCommonTable(**filtered_data)
    try:
        db.session.add(material_record)
        db.session.commit()
        material_common_id = material_record.id
        materials =None
        if form_data_dict["material_type"]=="Sensor":
            materials = [SensorTable(sensor_id=sensor_id,sensor_type=None,material_receiver_common_id=material_common_id) for sensor_id in form_data_dict["material_data"]["material_ids"]]
  

        elif form_data_dict["material_type"] == "FEH":
            materials = [
                FEHTable(
                    feh_id=feh_id,feh_type =None,
                    material_receiver_common_id=material_common_id
                ) 
                for feh_id in form_data_dict["material_data"]["material_ids"]
            ]

        elif form_data_dict["material_type"] == "SEH":
            materials = [
                SEHTable(
                    seh_id=seh_id,
                    material_receiver_common_id=material_common_id
                ) 
                for seh_id in form_data_dict["material_data"]["material_ids"]
            ]

        elif form_data_dict["material_type"] == "Main Bridge":
            materials = [
                MainBridgeTable(
                    main_bridge_id=bridge_id,
                    material_receiver_common_id=material_common_id
                ) 
                for bridge_id in form_data_dict["material_data"]["material_ids"]
            ]

        elif form_data_dict["material_type"] == "Stump Bridge":
            materials = [
                StumpBridgeTable(
                    stump_bridge_id=stump_id,
                    material_receiver_common_id=material_common_id
                ) 
                for stump_id in form_data_dict["material_data"]["material_ids"]
            ]

        elif form_data_dict["material_type"] == "Kapton Tapes":
            materials = [
                KaptonTapeTable(
                    kapton_id=kapton_id,
                    material_receiver_common_id=material_common_id
                ) 
                for kapton_id in form_data_dict["material_data"]["material_ids"]
            ]

        elif form_data_dict["material_type"] == "Glue":
            materials = [
                GlueTable(
                    glue_batch_id=glue_id,
                    expiry_date=datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date(),
                    material_receiver_common_id=material_common_id
                ) 
                for glue_id, expiry_date in zip(
                    form_data_dict["material_data"]["material_ids"], 
                    form_data_dict["material_data"]["expiry_dates"]
                )
            ]

        elif form_data_dict["material_type"] == "Wire Bonder":
            materials = [
                WireBonderTable(
                    expiry_date=datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date(),
                    spool_no=spool_number,
                    wedge_no=wedge_tool_number,
                    material_receiver_common_id=material_common_id
                ) 
                for  expiry_date, spool_number, wedge_tool_number in zip( 
                    form_data_dict["material_data"]["expiry_dates"], 
                    form_data_dict["material_data"]["spool_numbers"], 
                    form_data_dict["material_data"]["wedge_tool_numbers"]
                )
            ]
        elif form_data_dict["material_type"] == "Jig":
            materials = [
                JigTable(
                    name=jig_name,
                    material_receiver_common_id=material_common_id,
                    user_id = get_current_user_id()
                ) 
                for jig_name in  form_data_dict["material_data"]["material_ids"]
            ]
        elif form_data_dict["material_type"] == "VTRx":
            materials = [
                VTRxTable(
                    vt_rx_id=vt_rx_id,
                    material_receiver_common_id=material_common_id
                ) 
                for vt_rx_id in  form_data_dict["material_data"]["material_ids"]
            ]
        elif form_data_dict["material_type"] == "Ground Balancer":
            materials = [
                GroundBalancerTable(
                    ground_balancer_id=ground_balancer_id,
                    material_receiver_common_id=material_common_id
                ) 
                for ground_balancer_id in  form_data_dict["material_data"]["material_ids"]
            ]
        elif form_data_dict["material_type"] == "Other":
            materials = [
                OtherTable(
                    material_id=other_id,
                    material_receiver_common_id=material_common_id
                ) 
                for other_id in form_data_dict["material_data"]["material_ids"]
            ]

        else:
            print("Unknown material type")

        if materials:
            db.session.add_all(materials)
            db.session.commit()
            print("Materials added")
    except Exception as e:
        db.session.rollback()
        raise e
def save_burnin_test_data(data_dict):
    working_date = data_dict.get("workingDate")
    if not working_date:
        raise ValueError("Working date is required!")
    temp_humi_dew_id = save_temp_humi_dew_to_db({
        "temperature": float(data_dict.get("temperature", 0.0)),
        "dew_point": float(data_dict.get("dewPoint", 0.0)),
        "humidity": float(data_dict.get("humidity", 0.0))
    })

    date_time_id = save_datetime_to_db(working_date)

    module_id = int(data_dict["module_id"][0]) if isinstance(data_dict["module_id"], list) else int(data_dict["module_id"])

    # Create a new BurninTestTable record
    burnin_test_record = BurninTestTable(
        tracker_monitor_root_file=data_dict.get("tracker_monitor_root_file", None),
        tracker_root_file=data_dict.get("tracker_root_file", None),
        press_supply_root_file=data_dict.get("press_supply_root_file", None),
        burnin_box_root_file=data_dict.get("burnnin_box_root_file", None),
        comment=data_dict.get("comment", ""),
        all_module = str(data_dict["module_id"]),
        userid=get_current_user_id(),  # Function to fetch current user ID
        date_time_id=date_time_id,
        temp_humi_dew_id=temp_humi_dew_id,
        hybri_gluing_id=module_id,  # Hybrid gluing foreign key
        station_id=int(data_dict.get("station_name", 0))  # Convert station name to ID
    )

    # Add to session and commit
    db.session.add(burnin_test_record)
    db.session.commit()

    return burnin_test_record

def update_record(model, primary_id, field_name, new_value):
    try:
        record = db.session.get(model, primary_id) 
        if not record:
            return None  
        if not hasattr(record, field_name):
            raise AttributeError(f"Field '{field_name}' does not exist in {model.__name__}")
        
        setattr(record, field_name, new_value)  
        db.session.commit()  
        return record
    except Exception as e:
        db.session.rollback()
        raise e  
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)









