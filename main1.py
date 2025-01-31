'''
Import from line no : 7 to 80 
Login from 
'''

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



''' 
below  import all the forms required , which is defined in the forms.py
''' 

# --------------------------------------- Import forms , Data Base tables and Methods to save form to DataBase---

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
    BurNimForm,BurnimForm1, BurnimForm2, BurnimForm3, BurnimForm4, BurnimForm5, \
    BurnimForm6, BurnimForm7, BurnimForm8, BurnimForm9, BurnimForm10 ,
    ModuleData , SensorForm  ,WireBond,
    VTRxIDForm ,VTRxForm,GroundBalancerIDForm ,  GroundBalancerForm,
    FEHForm, SEHForm, MainBridgeForm, StumpBridgeForm, GlueForm, KaptonTapesForm, OpticalFibreForm, WireBonderForm, OtherConsumablesForm
      ,SensorIdListForm, FEHIdListForm, SEHIdListForm, MainBridgeIdListForm, StumpBridgeIdListForm, GlueBatchIdListForm, KaptonTapeIdListForm, OpticalFibreIdListForm, WireBonderDetailsForm, JigIDForm , OtherConsumablesListForm
)

''' 
now import all the stups related to the database tike the table and db , all are defined in the database_table.html

'''

#from database_table import User , Station , db
from database_table1 import (db , UserTable , DateTimeTable , StationTable , TempHumiDewTable ,MaterialReceivingCommonTable , SensorTable , FEHTable , SEHTable , MainBridgeTable , StumpBridgeTable ,
KaptonTapeTable , OtherTable , VTRxTable , GroundBalancerTable , GlueTable , WireBonderTable, VSensorTable, VFEHTable , VSEHTable,
VMainBridgeTable , VStumpBridgeTable , KaptonGluingTable , HVTable , IVTable , SensorGluingTable , NeedleMetrologyTable , SkeletonTestTable,
HybridGluingTable , ModuleEncapsulationTable , WireBondingTable , NoiseTest1Table , NoiseTest2Table , BurninTestTable )



from save_form_database1 import SaveFormToDataBase
from save_form_database import SaveToDataBase









# --------------------------- Import End -------------------------------------------------------------
# ------------------------------------ Defining Some Variables ---------------------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
utc_now = datetime.datetime.now()
current_date =f"{utc_now.year}-{utc_now.month}-{utc_now.day}" 
# make this dictionary for more readability once it works 
add_received_materials_forms = [SensorForm,FEHForm, SEHForm, 
                                MainBridgeForm, StumpBridgeForm, 
                                GlueForm, KaptonTapesForm, OpticalFibreForm,  
                                WireBonderForm,JigIDForm,OtherConsumablesForm,
                                VTRxForm,GroundBalancerForm]
material_receiver_data_dict = [{"sensor_id":[]},{"FEH_id":[]},{"SEH_id":[]},
                               {"main_bridge_id":[]},{"stump_bridge_id":[]},
                               {"glue_batch_id":[],"glue_expiry_date":[]},{"kapton_id":[]},{"optical_fibre_id":[]},
                               {"spool_no":[],"wedge_tool_no":[],"expiry_date":[]},{"jig_id":[]},{"other_id":[]}]
current_material_data = material_receiver_data_dict[0]
Material_receiver_ids_forms = [SensorIdListForm, FEHIdListForm, SEHIdListForm, MainBridgeIdListForm, StumpBridgeIdListForm, 
                               GlueBatchIdListForm, KaptonTapeIdListForm, OpticalFibreIdListForm, WireBonderDetailsForm,  
                               JigIDForm,OtherConsumablesListForm,VTRxIDForm,GroundBalancerIDForm]

# FORM_MAPPING_MATERIAL_RECEIVER = {
#     "sensor": SensorForm,
#     "FEH": FEHForm,
#     "SEH": SEHForm,
#     "main_bridge": MainBridgeForm,
#     "stump_bridge": StumpBridgeForm,
#     "glue": GlueForm,
#     "kapton_tapes": KaptonTapesForm,
#     "optical_fibre": OpticalFibreForm,
#     "wire_bonder": WireBonderForm,
#     "other": OtherConsumablesForm,
# }

FORM_MAPPING_VISUAL_INSPECTION = {
   "sensor_visual": SensorVisualForm,
    "FEH_visual": FEHVisualForm,
    "SEH_visual": SEHVisualForm,
    "main_bridge_visual": MainBridgeVisualForm,
    "stump_bridge_visual": StumpBridgeVisualForm,
}




'''
  create the flask object and follow some rules
'''
# ---------------------------- Flask App-------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
# define the Folder path here 

# app.config['UPLOAD_FOLDER'] = "static/uploads"

app.config["UPLOAD_WORKFLOW_FILES"]= "static/WORKFLOW_FILES"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
Bootstrap5(app)

db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "nisers.db")}'
db.init_app(app)
with app.app_context():
    db.create_all()

# -------------------------- Login part -------------------------------------------
#Flask log-in  ,this part is crucial for authenticaton 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return db.get_or_404(UserTable ,username)
@app.route('/login',methods =["GET","POST"])
# -------------------------- login button -----------------------------
@app.route('/')
def home_login():
    if not current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect(url_for('secrets'))

# ----------login user name and passwors fileds -----------------------
def login():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username)
        print(password)

        result = db.session.execute(db.select(UserTable).where(UserTable.username == username))
        
        user = result.scalar()
     
        if user:
            if not user.is_active:
                flash("Your account is inactive. Please contact support.")
                return redirect(url_for('login'))

            # Verify password
            # if check_password_hash(user.password, password): --------------------check this out ---------
            # later use the above if you want to read hash 
            if user.password == password:
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                flash("Incorrect password, please try again.")
        else:
            flash("User does not exist, please check your email.")
    return render_template("login.html")
# -------------------- user logout -------------------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
# ------------------------ --------------------------------------------------------

# -------------------------- HOME (WORKFLOW and MODULES) -------------------------------------------------------------------------------
@app.route('/secrets')
@login_required
def secrets():
    return render_template("home.html")

# ----------------------------MODULES---------------------------------------------------------------------------
@app.route('/modules')
@login_required
def show_module():
    return render_template("modules.html")

# ---------when you click on a specific module id this method is executed and module_report.html corresponding to that module will# be rendered and it is under ..
@app.route('/module_report')
@login_required
def module_report():
    return render_template("module_report.html")

# ----- download module report page -----------
@app.route('/download')
@login_required
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")

# --------------------------Stations----------------------------------------------------------------------------

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
        new_station = StationTable(station_name = station_name,
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


# --------------------------------------WORKFLOW-----------------------------------------------------------

'''
 here the main thing comes , in the workflow page when you select a process , the num gets it's value which is defined in the workflow.html have a look , that number will tell(see the logic below)  which form to show and after we have to save the data entered in the form to the database once the form is validated 
  Also the visual_inspection.html renders the form
'''
# ------workflow steps -------------------- 
@app.route('/workflow')
@login_required
def work_flow():
    return render_template("workflow.html")
# ------ Showing form ---------------------
@app.route('/add_data', methods=["GET", "POST"])
def add_data():
    num = request.args.get('num')
    if not num:
        print("num variable didn't come correctly ")
        num = 0
    # Better define in each workflow step ................
    step_no = int(num)
    sensor_ids = ["efwe321","semd3244","sensor4"]
    bare_module_ids = ["bare1","bare2","bare3"]
    module_ids = ["module1","module2"]
    skeleton_ids = ["module3","module4"]
    # ....................................................
    # ...............WorkFlow(Material_Receiver)..........
    if step_no == 0:
        # dynamic form requirement 
        # show all the material receiver category then goto add_materials
        return render_template("material_type.html")
    # ...............WorkFlow(Visual_Inspection)..........
    elif step_no == 1:
        # Select Material type then go 'visual_inspection_data' 
        return render_template("visual_type.html")
    # ...............WorkFlow(KaptonGluing)...............
    elif step_no == 2:
        # render Kapton Gluing form give sensor choices  , static Form 
        form = KaptonGluing()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            '''
            buind the logic to get the data and save it the database
            '''
            SaveToDataBase().save_kapton_gluing_form(form,db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))  
    elif step_no == 3:
        # Needs Sensor choices , Static Form 
        form = HvForm()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            '''
            Biuld the logic here to save the form in the database 
            '''
            SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 31:
        # static form 
        form = IvForm()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            '''
            Biuld the logic here to save the form in the database 
            '''
            SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 4:
        # static form , TOP and Bottom sensor Table 
        form = SensorGluing()
        form.top_sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        form.bottom_sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            '''
            Biuld the logic here to save the form in the database 
            '''
            SaveToDataBase().save_sensor_gluing_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 5:
        # static 
        form = NeedleMetrologyForm()
        form.bare_module_id.choices = [(bare_module.bare_module_id, bare_module.bare_module_id) for bare_module in bare_module_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_needle_metrology_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 6:
        form = SkeletonTestForm()
        if form.validate_on_submit():
            SaveToDataBase().save_skeleton_test_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 7:
        form = HybridGluingForm()
        form.bare_module_id.choices = [(bare_module.bare_module_id, bare_module.bare_module_id) for bare_module in bare_module_ids]
        form.skeleton_id.choices =[(skeleton.skeleton_id, skeleton.skeleton_id) for skeleton in skeleton_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_hybrid_gluing_form( form ,db ,app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 71:
        form = ModuleEncapsulationForm()
        if form.validate_on_submit():
            print("module encapsulation form is validated ")
            return redirect(url_for('work_flow'))
    elif step_no == 11:
        form = ModuleData()
    elif step_no == 8:  # Wire Bonding
        # Dynamic Form 
        template_name = "wire_bonding.html"  # Use a unique template for Wire Bonding
        return redirect(url_for('wire_bonding'))
    elif step_no == 9:
        form = NoiseTestForm_Ph2_ACF()
        form.module_id.choices = [(module.module_id, module.module_id) for module in module_ids]
        if form.validate_on_submit():
            pass  
    elif step_no == 10:
        form = BurNimForm()
        if form.validate_on_submit():
            module_quantity = int(form.module_quantity.data)
            return redirect(url_for('burnim_data_upload',module_quantity = module_quantity))
    
    return render_template("visual_inspection.html", form=form)

# -------------WorkFlow_MaterialReceiver_Common addformData ------------------------------------------

@app.route('/add_received_materials', methods = ["GET","POST"])
def add_received_materials():
    # get material receiving type from material_type.html 
    index_number = int(request.args.get("num"))
    # This part for adding jig 
    if index_number == 9:
       return redirect(url_for('add_material_ids' ))
    
    basic_form = add_received_materials_forms[index_number]()
    #session['basic_form_data'] = basic_form.data
    session['index_number'] = index_number
    if basic_form.validate_on_submit():
        print("basic form is validated ")
        current_material_data = material_receiver_data_dict[index_number]
        return redirect(url_for('add_material_ids' ))
    return render_template("visual_inspection.html", form=basic_form)
@app.route('/add_material_ids',methods = ["GET","POST"])
def add_material_ids():
    index_number = session.get('index_number')
    if index_number is None or index_number >= len(Material_receiver_ids_forms):
        return "Invalid index number", 400

    id_form = Material_receiver_ids_forms[index_number]
    
    #basic_form_data = request.args.get('basic_form_data')
    #print("----is it None",basic_form_data)
    # get a dict , save the 
    if request.method == "POST":
        # Get data from AJAX request
        form = id_form(request.form)
        for fieldlist in form:
            try:
                _ = (entry for entry in fieldlist)
            except TypeError:
                print("got type error ")
                print(fieldlist.name, fieldlist.data)
                continue
            for entry in fieldlist:
                print(entry.name, entry.data)
        # Server-Side Validation
        if id_form().validate():
            print(id_form().data)
            print("form is validated ")
            # Valid data -  Can be saved to a database
            return form.data
        else:
            # Validation Failed
            return 'Data not saved!'
    return render_template('dynamic_form.html', form=id_form())
    # if request.method == "POST":
    #     form = Material_receiver_ids_forms[index_number]()
    #     for fieldlist in form:
    #         try:
    #             _ = (entry for entry in fieldlist)
    #         except TypeError:
    #             print("got some type error")
    #             print(fieldlist.name,fieldlist.data)
    #             continue
    #         for entry in fieldlist:
    #             print(entry.name , entry.data)
    # if id_form.validate():
    #     print("id form submitted")
    #     print(id_form.data)
    #     return redirect(url_for("work_flow"))
    # print("after--------------")
    # return render_template("dynamic_form.html", form=id_form ,data_post_url = 'add_material_ids',type= type )
    
    '''
    if not form_class:
        return f"Invalid material_type: {material_type}", 400  # Return an error if the type is invalid
    
    # Create an instance of the form
    form = form_class()
    
    # Validate and process the form submission
    if form.validate_on_submit():
        print("Validating form in add_materials route")
        print(form.data)
        
        # Process specific fields for SensorForm as an example
        if material_type == "sensor":
            for item in form.sensor_id.data:
                print("Sensor ID:", item)
        
        # Example of returning the uploaded file name
        return f"Uploaded file: {form.sensor_img.data.filename}"
    
    # Render the template with the dynamically chosen form
    '''
    return render_template("visual_inspection.html", form=form)
'''
def add_materials():
    material_type = request.args.get("material_type")
    form = SensorForm()
    
    if form.validate_on_submit():
        sensor_img = request.files.get('sensor_img')
        if sensor_img:
            filename = secure_filename(sensor_img.filename)
        print("validating form in test route")
        print(form.data)
        for item in form.sensor_id.data:
            print("lastnames",item) 
        return form.sensor_img.data.filename
    return render_template("dynamic_form.html", form=form)
    #return redirect(url_for('add_data',num = 0))
'''
# < ---------------------- Visual Inspection Part ------------------------------
@app.route('/visual_inspection_data', methods=["GET", "POST"])
def visual_inspection_data():
    # get the material type name from  visual_type.html 
    material_type = request.args.get("material_type")
    # get the corresponding form from FORM_MAPPING_VISUAL_INSPECTION (dict)
    visual_material_form = FORM_MAPPING_VISUAL_INSPECTION[material_type]()
    if visual_material_form.validate_on_submit():
        SaveFormToDataBase(app.config["UPLOAD_WORKFLOW_FILES"],db).save_VSensor(visual_material_form,file_name="vsensor.png",user_id=1)
        return redirect('work_flow')
    return render_template("visual_inspection.html",form = visual_material_form)
    

@app.route('/sensor_inspection', methods=["GET", "POST"])
def sensor_inspection():
    form = VisualInspectionSensor()
    if form.validate_on_submit():
        sensor_id = form.sensor_id.data
        sensor_image = form.sensor_image.data
        comment = form.comment.data
        image_url = save_get_file_url(sensor_image)
        new_sensor_inspection = VisualInspectionSensorTable(
                                          sensor_id = sensor_id,
                                          sensor_image = image_url,
                                          comment = comment )
        db.session.add(new_sensor_inspection)
        db.session.commit()
        return redirect(url_for('work_flow'))
    return render_template("visual_inspection.html", form=form)
@app.route('/hybrid_inspection', methods=["GET", "POST"])
def hybrid_inspection():
    form = VisualInspectionHybrid()
    if form.validate_on_submit():
        hybrid_id = form.hybrid_id.data
        hybrid_image = form.hybrid_image.data
        comment = form.comment.data
        image_url = save_get_file_url(hybrid_image)
        new_hybrid_inspection = VisualInspectionHybridTable(
                                          hybrid_id = hybrid_id,
                                          hybrid_image = image_url,
                                          comment = comment )
        db.session.add(new_hybrid_inspection)
        db.session.commit()
        return redirect(url_for('work_flow'))
    return render_template("visual_inspection.html", form=form)
@app.route('/bridge_inspection', methods=["GET", "POST"])
def bridge_inspection():
    form = VisualInspectionBridge()
    if form.validate_on_submit():
        SaveToDataBase().save_visual_inspection_bridge_form(form ,db ,app.config['UPLOAD_WORKFLOW_FILES'])
        return redirect(url_for('work_flow'))
    return render_template("visual_inspection.html", form=form)

# ------------------ Visual Inspection End ----------------------

@app.route('/burnim_data_upload', methods=["GET", "POST"])
def burnim_data_upload():
    module_ids = db.session.query(HybridGluingTable.module_id).distinct().all()
    module_quantity = int(request.args.get('module_quantity', 1))  
    form = None
    if module_quantity == 1:
        form = BurnimForm1(module_ids)
    elif module_quantity == 2:
        form = BurnimForm2(module_ids)
    elif module_quantity == 3:
        form = BurnimForm3(module_ids)
    elif module_quantity == 4:
        form = BurnimForm4(module_ids)
    elif module_quantity == 5:
        form = BurnimForm5(module_ids)
    elif module_quantity == 6:
        form = BurnimForm6(module_ids)
    elif module_quantity == 7:
        form = BurnimForm7(module_ids)
    elif module_quantity == 8:
        form = BurnimForm8(module_ids)
    elif module_quantity == 9:
        form = BurnimForm9(module_ids)
    elif module_quantity == 10:
        form = BurnimForm10(module_ids)

    
    if form and form.validate_on_submit():
        SaveToDataBase().save_burnim_test_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'], module_quantity)
        return redirect(url_for('work_flow'))

    return render_template("visual_inspection.html", form=form)

    # if form.validate_on_submit():
    #     # Handle the form submission logic here
    #     flash(f"Step {step_no} data submitted successfully!", "success")
    #     return redirect(url_for('workflow'))  # Redirect to workflow after submission

    # return render_template(template_name, form=form)
@app.route('/wire_bonding', methods=['GET', 'POST'])
@login_required
def wire_bonding():
    if request.method == 'POST':
        # Debugging: Print all form data
        print("\n=== FORM DATA RECEIVED ===")
        for key, value in request.form.items():
            print(f"{key}: {value}")

        # Debugging: Print file upload information
        print("\n=== FILE UPLOADS ===")
        for file_key in request.files:
            file = request.files[file_key]
            if file.filename != '':
                print(f"Uploaded file: {file_key} => {file.filename}")
                # Read file content for debugging (without saving)
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                print(f"File size: {size} bytes")
            else:
                print(f"Empty file upload: {file_key}")

        # Process Module ID and Parameters
        module_id = request.form.get('module_id')
        print(f"\nProcessing Module ID: {module_id}")

        # Process Top Parameters
        top_params = {
            'delta_height': request.form.get('top_delta_height'),
            'correction_factor_k1': request.form.get('top_correction_factor_k1'),
            'correction_factor_k2': request.form.get('top_correction_factor_k2'),
            'mean_force_1': request.form.get('top_mean_force_1'),
            'mean_force_2': request.form.get('top_mean_force_2'),
            'rms_value': request.form.get('top_rms_value'),
            'standard_deviation': request.form.get('top_standard_deviation')
        }
        print("\nTop Parameters:", top_params)

        # Process Bottom Parameters
        bottom_params = {
            'delta_height': request.form.get('bottom_delta_height'),
            'correction_factor_k1': request.form.get('bottom_correction_factor_k1'),
            'correction_factor_k2': request.form.get('bottom_correction_factor_k2'),
            'mean_force_1': request.form.get('bottom_mean_force_1'),
            'mean_force_2': request.form.get('bottom_mean_force_2'),
            'rms_value': request.form.get('bottom_rms_value'),
            'standard_deviation': request.form.get('bottom_standard_deviation')
        }
        print("\nBottom Parameters:", bottom_params)

        # Process Dynamic Rows
        def process_table_data(prefix):
            data = []
            i = 1
            while True:
                # Check if at least one field exists for this row
                if not request.form.get(f'{prefix}_raw_pull_force_{i}'):
                    break
                
                row_data = {
                    'raw_pull_force': request.form.get(f'{prefix}_raw_pull_force_{i}'),
                    'distance_between_feet': request.form.get(f'{prefix}_distance_between_feet_{i}'),
                    'type_of_break': request.form.get(f'{prefix}_type_of_break_{i}'),
                    'correction_factor': request.form.get(f'{prefix}_correction_factor_{i}'),
                    'corrected_force': request.form.get(f'{prefix}_corrected_force_{i}'),
                    'comment': request.form.get(f'{prefix}_comment_{i}')
                }
                data.append(row_data)
                print(f"\n{prefix.capitalize()} Row {i}:")
                print(json.dumps(row_data, indent=2))
                i += 1
            return data

        # Process Top and Bottom Tables
        print("\nPROCESSING TOP TABLE DATA:")
        top_data = process_table_data('top')
        print("\nPROCESSING BOTTOM TABLE DATA:")
        bottom_data = process_table_data('bottom')

        flash("Wire Bonding data submitted successfully!", "success")
        return redirect(url_for('work_flow'))
        return redirect(url_for('work_flow'))

    form = WireBondingForm()
    return render_template('wire_bonding.html', form=form)


'''
 this portion is the activated when stations is clicked basically it shows all the stations that are available in the database and gives a options to add more stations 
'''
# -------------------------------- Additional Methods -----------------------------------
# Define save_get_file_url function which take the the form file data , save the data in a given folder and returns path
def save_get_file_url(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_WORKFLOW_FILES'],filename)
    file.save(file_path)
    return file_path

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# create all the tables 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)









