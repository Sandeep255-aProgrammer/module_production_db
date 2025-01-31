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
import openpyxl

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
    NoiseTestForm,
    BurninForm,BurninForm1, BurninForm2, BurninForm3, BurninForm4, BurninForm5, \
    BurninForm6, BurninForm7, BurninForm8, BurninForm9, BurninForm10 ,
    ModuleData , SensorForm  ,WireBond,
    VTRxIDForm ,VTRxForm,GroundBalancerIDForm ,  GroundBalancerForm,
    FEHForm, SEHForm, MainBridgeForm, StumpBridgeForm, GlueForm, KaptonTapesForm, OpticalFibreForm, WireBonderForm, OtherConsumablesForm
      ,SensorIdListForm, FEHIdListForm, SEHIdListForm, MainBridgeIdListForm, StumpBridgeIdListForm, GlueBatchIdListForm, KaptonTapeIdListForm, OpticalFibreIdListForm, WireBonderDetailsForm, JigIDForm , OtherConsumablesListForm
)
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

''' 
now import all the stups related to the database tike the table and db , all are defined in the database_table.html

'''

#from database_table import User , Station , db
#TO DO: Need to change the import statement to import all the tables from database_table.py
from database_table import (
    db ,
    User,
    Station ,
    MaterialReceiverTable,
    VisualInspectionSensorTable,
    VisualInspectionHybridTable,
    VisualInspectionBridgeTable,
    KaptonGluingTable,
    HvIvFormTable,
    SensorGluingTable,
    NeedleMetrologyTable,
    SkeletonTestTable,
    HybridGluingTable,
    ModuleDataTable,
    WireBondingTable,
    NoiseTestTable,
    BurninTable


)


from save_form_database import SaveToDataBase


'''
  create the flask object and follow some rules
'''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
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

    

#Flask log-in  ,this part is crucial for authenticaton 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return db.get_or_404(User ,username)

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

@app.route('/wire_bonding', methods=['GET', 'POST'])
@login_required
def wire_bonding():
    if request.method == 'POST':
        ###################Debugging start####################################

        print("\n=== FORM DATA RECEIVED ===")
        for key, value in request.form.items():
            print(f"{key}: {value}")

        # Debugging: Print file upload information
        print("\n=== FILE UPLOADS ===")
        for file_key in request.files:
            file = request.files[file_key]
            if file.filename != '':
                print(f"Uploaded file: {file_key} => {file.filename}")
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                print(f"File size: {size} bytes")
            else:
                print(f"Empty file upload: {file_key}")
        ###################Debugging end####################################

        module_id = request.form.get('module_id')
        temperature = request.form.get('temperature')
        dewpoint = request.form.get('dewpoint')
        humidity = request.form.get('humidity')
        comment = request.form.get('comment')
        print(f"\nModule ID: {module_id}, Temperature: {temperature}, Dewpoint: {dewpoint}, Humidity: {humidity}")

        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)  
                print(f"Image saved to: {image_path}")

        # Function to process correction factors and forces
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

        #Top and Bottom Parameters
        top_params = process_parameters('top')
        bottom_params = process_parameters('bottom')
        print("\nTop Parameters:", top_params)
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

        print("\nPROCESSING TOP TABLE DATA:")
        top_data = process_table_data('top')
        print("\nPROCESSING BOTTOM TABLE DATA:")
        bottom_data = process_table_data('bottom')

        # Saving in excel file
        try:
            file_path = 'wire_bonding_data.xlsx'
            workbook = openpyxl.load_workbook(file_path)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()

        # Save table data to another sheet if needed
        sheet = workbook.create_sheet(title='Top Data')
        sheet.append(['Raw Pull Force', 'Distance Between Feet', 'Type of Break',
                       'Correction Factor', 'Corrected Force', 'Comment'])
        for row in top_data:
            sheet.append(list(row.values()))

        sheet2 = workbook.create_sheet(title='Bottom Data')
        sheet2.append(['Raw Pull Force', 'Distance Between Feet', 'Type of Break',
                       'Correction Factor', 'Corrected Force', 'Comment'])
        for row in bottom_data:
            sheet2.append(list(row.values()))

        workbook.save(file_path)

        data_dict = {
            'module_id': module_id,
            'temperature': temperature,
            'dewpoint': dewpoint,
            'humidity': humidity,
            'comment': comment,
            'image_path': image_path,
        }


        flash("Wire Bonding data submitted successfully!", "success")
        return redirect(url_for('work_flow'))


    form = WireBondingForm()
    return render_template('wire_bonding.html', form=form)


'''
 this portion is the activated when stations is clicked basically it shows all the stations that are available in the database and gives a options to add more stations 
'''

@app.route('/stations')
@login_required
def stations():
    with app.app_context():
        result = db.session.execute(db.select(Station).order_by(Station.id))
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
        new_station = Station(station_name = station_name,
                              station_location = station_location,
                              created_at = station_created_at,
                              remarks = station_remarks,
                              img_path = img_path,
                              is_active = station_is_active,
                              iteration_number = station_iteration_number, 
                              operator = station_operator)
        db.session.add(new_station)
#iteration_number = station_iteration_number,
        db.session.commit()
        return redirect(url_for('stations'))
# this steps make sure the operator filed is auto filled with by the current user name 
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
    workflow_name = request.args.get('workflow_name', 'Workflow')
    if not num:
        num = 0
    step_no = int(num)
    sensor_ids = db.session.query(VisualInspectionSensorTable.sensor_id).distinct().all()
    bare_module_ids = db.session.query(SensorGluingTable.bare_module_id).distinct().all()
    module_ids = db.session.query(HybridGluingTable.module_id).distinct().all()
    skeleton_ids = db.session.query(SkeletonTestTable.skeleton_id).distinct().all()

    if step_no == 0 :
        # Log each field for debugging  
        print("\n=== FORM DATA RECEIVED ===")
    
        # Extracting general form details
        received_from = request.form.get('received_from', 'Unknown')
        date = request.form.get('date', 'Unknown')
        temperature = request.form.get('temperature', 'Unknown')
        humidity = request.form.get('humidity', 'Unknown')
        dew_point = request.form.get('dew_point', 'Unknown')
        material_types = request.form.getlist('material_type[]')
        material_comment = request.form.get('material_comment', '')

        # Print general form details
        print(f"Received From: {received_from}")
        print(f"Date: {date}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Dew Point: {dew_point}°C")
        print(f"{', '.join(set(material_types))} Comment: {material_comment}")

        print("\n=== FILE UPLOADS ===")
        for file_key in request.files:
            file = request.files[file_key]
            if file.filename:
                print(f"Uploaded file: {file_key} => {file.filename}")
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                print(f"File size: {size} bytes")
            else:
                print(f"Empty file upload: {file_key}")

        print("\n=== MATERIAL ENTRIES ===")

        # Retrieve multiple materials
        material_ids = request.form.getlist('material_id[]')
        expiry_dates = request.form.getlist('expiry_date[]')
        spool_numbers = request.form.getlist('spool_number[]')
        wedge_tool_numbers = request.form.getlist('wedge_tool_no[]')

        # Ensure all entries are printed
        
        for i in range(len(material_ids)):  # Iterate over all rows
            material_id = material_ids[i] if i < len(material_ids) else "Unknown"
            material_type = material_types[i] if i < len(material_types) else "Unknown"
            expiry_date = expiry_dates[i] if i < len(expiry_dates) else "N/A"
            spool_no = spool_numbers[i] if i < len(spool_numbers) else "N/A"
            wedge_tool_no = wedge_tool_numbers[i] if i < len(wedge_tool_numbers) else "N/A"

            print(f"\nMaterial Entry {i + 1}:")
            print(f"{material_type} ID: {material_id}")

            if material_type == "Glue":
                print(f"Expiry Date: {expiry_date}")

            elif material_type == "Wire Bonder":
                print(f"Spool Number: {spool_no}, Wedge Tool No.: {wedge_tool_no}, Expiry Date: {expiry_date}")

        return render_template("material_reciever.html")

        # form = MaterialReceiverTypeForm()
        # if form.validate_on_submit():
        
        #     material_type = form.material_type.data
        #     return redirect(url_for('add_materials',material_type=material_type))
        #     sensors_quantity = form.sensors_quantity.data
        #     hybrid_quantity = form.hybrid_quantity.data
        #     optical_fibres_quantity = form.optical_fibres_quantity.data
        #     kaptontapes_quantity = form.kaptontapes_quantity.data
        #     bridges_quantity = form.bridges_quantity.data
        #     others = form.others.data
        #     receiver_name = form.receiver_name.data
        #     #date = form.date.data
        #     image = form.image.data
        #     comment = form.comment.data
        #     if image and image.filename != '':
        #         image_url = save_get_file_url(image)
        #     else:
        #         image_url = None
        #     new_material_receiving = MaterialReceiverTable(
        #                                sensors_quantity = sensors_quantity ,
        #                                hybrid_quantity = hybrid_quantity ,
        #                                optical_fibres_quantity = optical_fibres_quantity ,
        #                                kaptontapes_quantity = kaptontapes_quantity ,
        #                                receiver_name = receiver_name,
        #                                bridges_quantity = bridges_quantity ,
        #                                others = others ,
                                       
        #                                image_url = image_url , comment = comment )
        #     db.session.add(new_material_receiving)
        #     db.session.commit()
        #     return redirect(url_for('work_flow'))
        #     return render_template("material_reciever.html", form=form)
        
       
    
    elif step_no == 1:

        form = VisualInspection()
        inspection_number = None
        if form.validate_on_submit():
            inspection_number = int(form.inspection_type.data)
            if inspection_number == 1:
                return redirect(url_for('sensor_inspection'))
            elif inspection_number == 3:
                return redirect(url_for('hybrid_inspection'))
            elif inspection_number == 2:
                return redirect(url_for('bridge_inspection'))
        return render_template("visual_inspection.html", form=form, process_name=workflow_name) 
            

        return render_template("visual_type.html")

    elif step_no == 2:
        form = KaptonGluing()
        # add sensor ids from VisualInspectionsencor table to the sensor id choices 
        #sensor_ids = db.session.query(VisualInspectionSensorTable.sensor_id).distinct().all()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_kapton_gluing_form(form,db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
        
        
    elif step_no == 3:
        form = HvForm()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 31:
        form = IvForm()
        form.sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_hv_iv_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 4:
        form = SensorGluing()
        form.top_sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        form.bottom_sensor_id.choices = [(sensor.sensor_id, sensor.sensor_id) for sensor in sensor_ids]
        if form.validate_on_submit():
            SaveToDataBase().save_sensor_gluing_form(form, db, app.config['UPLOAD_WORKFLOW_FILES'])
            return redirect(url_for('work_flow'))
    elif step_no == 5:
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
        #form = WireBondingForm()
        template_name = "wire_bonding.html"  # Use a unique template for Wire Bonding
        return redirect(url_for('wire_bonding'))
    elif step_no == 9:
        form = NoiseTestForm_Ph2_ACF()
        form.module_id.choices = [(module.module_id, module.module_id) for module in module_ids]
        if form.validate_on_submit():
            pass
          
    elif step_no == 10:
        form = BurninForm()
        if form.validate_on_submit():
            module_quantity = int(form.module_quantity.data)
            return redirect(url_for('burnin_data_upload',module_quantity = module_quantity))
    
    return render_template("visual_inspection.html", form=form, process_name=workflow_name)



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

                print(entry.name , entry.data)
    if id_form.validate():
        print("id form submitted")
        print(id_form.data)
        return redirect(url_for("work_flow"))
    print("after--------------")
    return render_template("dynamic_form.html", form=id_form ,data_post_url = 'add_material_ids',type= type )


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
@app.route('/burnin_data_upload', methods=["GET", "POST"])
def burnin_data_upload():
    module_ids = db.session.query(HybridGluingTable.module_id).distinct().all()
    module_quantity = int(request.args.get('module_quantity', 1))  
    form = None
    if module_quantity == 1:
        form = BurninForm1(module_ids)
    elif module_quantity == 2:
        form = BurninForm2(module_ids)
    elif module_quantity == 3:
        form = BurninForm3(module_ids)
    elif module_quantity == 4:
        form = BurninForm4(module_ids)
    elif module_quantity == 5:
        form = BurninForm5(module_ids)
    elif module_quantity == 6:
        form = BurninForm6(module_ids)
    elif module_quantity == 7:
        form = BurninForm7(module_ids)
    elif module_quantity == 8:
        form = BurninForm8(module_ids)
    elif module_quantity == 9:
        form = BurninForm9(module_ids)
    elif module_quantity == 10:
        form = BurninForm10(module_ids)

    
    if form and form.validate_on_submit():
        SaveToDataBase().save_burnin_test_form( form, db, app.config['UPLOAD_WORKFLOW_FILES'], module_quantity)
        return redirect(url_for('work_flow'))

    return render_template("visual_inspection.html", form=form)

'''
# if form.validate_on_submit():
#     # Handle the form submission logic here
#     flash(f"Step {step_no} data submitted successfully!", "success")
#     return redirect(url_for('workflow'))  # Redirect to workflow after submission

#     return render_template(template_name, form=form)






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)









