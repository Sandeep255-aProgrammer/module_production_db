from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import Form , DecimalField ,IntegerField ,StringField, SubmitField, PasswordField ,FileField ,DateField , BooleanField , SelectField,  DateTimeField,FormField, FloatField , FieldList,TextAreaField
from wtforms.validators import DataRequired, URL, Optional
from flask_ckeditor import CKEditorField



'''
This is the py file for making forms , it is based on wtforms module so visit the website to learn more about this module like fields , FileField etc 


'''

# < ------------------ Authentication forms ------------------------------
# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

# ----------------------- Authentication form ends --------------------------->
# --------------------------stations Form start -----------------------------> 
# create Station Add forms
class AddStationForm(FlaskForm):
    station_name = StringField("Station Name", validators=[DataRequired()])
    station_img = FileField("Upload the Station Image", validators=[DataRequired()])
    
    station_created_at = DateTimeField("Created At (%Y-%m-%d %H:%M:%S)", format='%Y-%m-%d %H:%M:%S')
    station_location = StringField("Station Location", validators=[DataRequired()])
    station_is_active = BooleanField("Is station active in this status")
    station_operator = StringField("Operator", validators=[DataRequired()])
    station_iteration_number = StringField("Iteration Number", validators=[DataRequired()])
    station_remarks = TextAreaField("Remarks", validators=[DataRequired()])
    submit= SubmitField("Save Station")

    # Link to the User table via the `username` field
    #operator: Mapped[str] = mapped_column(String(100), ForeignKey("Users.username"), nullable=False)
#-------------------------- stations Form End -------------------------------->


#---------------------- Visual Inspection Form Start(workflow ) -------------------------------------- 
# VisualInspectionForm done

class SensorVisualForm(FlaskForm):
    material_id = SelectField("Sensor ID", validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
class FEHVisualForm(FlaskForm):
    material_id = SelectField("FEH ID", validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
class SEHVisualForm(FlaskForm):
    material_id = SelectField("SEH ID", validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
class MainBridgeVisualForm(FlaskForm):
    material_id = SelectField("Main Bridge ID", validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
class StumpBridgeVisualForm(FlaskForm):
    material_id = SelectField("Stump Bridge ID", validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# <-------------------------- Kapton Gluing Form (workflow ) ------------------------------------

class KaptonGluing(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    sensor_id = SelectField("Sensor ID", validators=[DataRequired()])
    sensor_type = SelectField(
        'Sensor Type',
        choices=[('Top Sensor', 'Top Sensor'), ('Bottom Sensor', 'Bottom Sensor')],
        validators=[DataRequired()]
    )
    station = SelectField("Station", validators=[DataRequired()])

    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    part_A_batch_no = SelectField("Polytec 601 partA / Batch No :")
    # part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])# auto fill
    part_B_batch_no = SelectField("Polytec 601 partB / Batch No :")
    # part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()]) # auto fill
    jig_id = SelectField("Select Jig No.",validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    image = FileField("Upload Image (optional)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# ------------------------------Kapton Gluing End Form --------------------------------->

#------------------------------ HVIV Form (WorkFlow)------------------------------------->
class HvForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    sensor_id = SelectField("Sensor ID", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()])#auto
    hv_csv = FileField("HV CSV" ,validators=[DataRequired()])
    
  # upload csv
    
    image = FileField("Upload Image(optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
class IvForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    sensor_id = SelectField("Sensor ID", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()])#auto

    iv_csv =  FileField("IV CSV" ,validators=[DataRequired()])
  # upload csv
    
    image = FileField("Upload Image(optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# ---------------------  HVIV form End------------------------------------------------>

# ------------------------- Sensor Gluing Form start (workflow) ----------------------->

class SensorGluing(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    bare_module_id = StringField("Bare_Module ID/Name", validators=[DataRequired()])
    top_sensor_id = SelectField("Top Sensor ID", validators=[DataRequired()])
    bottom_sensor_id = SelectField("Bottom Sensor ID", validators=[DataRequired()])
    main_bridge_id = SelectField("Main Bridge ID", validators=[DataRequired()])
    stump_bridge_id = SelectField("Stump Bridge ID", validators=[DataRequired()])
    module_spacing =  SelectField("Module Spacing" ,choices=[('1.8mm' , '1.8mm')],validators=[DataRequired()])
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    jig_id  = SelectField("Jig Id.", validators=[DataRequired()])
    part_A_batch_no = SelectField("Polytec TC437 partA / Batch No :")
    part_B_batch_no = SelectField("Polytec TC437 partB / Batch No :")
    station = SelectField("Station", validators=[DataRequired()])
    image = FileField("Upload Image")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# -------------------------- Sensor Gluing Form End --------------------------->

# ---------------------------- Needlr Metrology form start (workflow)-------------------->

class NeedleMetrologyForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    bare_module_id = SelectField("Bare_Module ID", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    x_coordinate = StringField("Delta x", validators=[DataRequired()])
    y_coordinate = StringField("Delta y", validators=[DataRequired()])
    del_theta = StringField("Rotation", validators=[DataRequired()])
    csv_excel= FileField("Upload Data (csv/excel)" ,validators=[DataRequired()])
    image = FileField("Upload Image (optional)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# --------------------------  Needle Metrology Form End (workflow)--------------------->

# <-------------------------- SkeletonTest START (Workflow) ----------------------------

class SkeletonTestForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    skeleton_id = StringField("Skeleton ID", validators=[DataRequired()])
    FEH_L =  SelectField("FEH_LID", validators=[DataRequired()])
    FEH_R = SelectField("FEH_RID", validators=[DataRequired()])
    SEH = SelectField("SEH",validators=[DataRequired()])
    VTRx = SelectField("VTRx+_ID", validators=[DataRequired()])
    ground_balancer_id = SelectField("Ground Balancer ID", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    file = FileField("Upload File ",validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# ----------------------- SkeletonTest End ---------------------------------------- >

# <------------------------  Hybrid Test Form Start (workflow)-----------------------

class HybridGluingForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = StringField("Module ID", validators=[DataRequired()])
    bare_module_id = SelectField("Bare_Module ID", validators=[DataRequired()])
    skeleton_id = SelectField("Skeleton ID", validators=[DataRequired()])
    part_A_batch_no = SelectField("Polytec TC437 partA / Batch No :")
    part_B_batch_no = SelectField("Polytec TC437 partB / Batch No :")
    station = SelectField("Station", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# ------------------------ Hybrid Test Form End ---------------------------------------->

#------------------------- Moudle Encapsulation Form ----------------------------------

class ModuleEncapsulationForm(FlaskForm):
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = SelectField("Module ID (Select)", validators=[DataRequired()])
    glue_a = SelectField("Glue A", validators=[DataRequired()])
    glue_b = SelectField("Glue B", validators=[DataRequired()])
    glue_preparation_time = StringField("Glue Preparation Time", validators=[DataRequired()])
    jig = SelectField("Jig", validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    img = FileField("Upload Image (Optional)")
    submit = SubmitField("Save")

#-------------------------------- Module Encap. End Form ------------------------------->

# <------------------------ Module Save Form Start (workflow)---------------------------

class ModuleData(FlaskForm):
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = SelectField("Module_ID", validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# --------------------- Module Save form End -------------------------------------------->

# <---------------------- Wire Bonding Form Start (workflow) -----------------------------


class WireBondingForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# ------------------------- Wire Bond Form End ----------------------------------------->

# <------------------------- NoiseTestForm Start (workflow)----------------------------

class NoiseTestForm_Ph2_ACF(FlaskForm):
    temp = FloatField("Temperature (°C):", validators=[DataRequired()])
    humidity = FloatField("Humidity:", validators=[DataRequired()])
    dew_point = FloatField("Dew Point:", validators=[DataRequired()])
    working_date = DateField("Working Date:", validators=[DataRequired()])
    module_id = SelectField("Module ID:",validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    upload_folder1 = FileField("Aldrino File:",validators=[DataRequired()])
    upload_folder2 = FileField("HV File:",validators=[DataRequired()])
    upload_folder3 = FileField("LV File:",validators=[DataRequired()])
    upload_folder4 = FileField("IV File:",validators=[DataRequired()])
    upload_folder5 = FileField("ROOT File:",validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit= SubmitField("Save")
class NoiseTestForm_GIPHT(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = SelectField("Module ID",validators=[DataRequired()])
    station = SelectField("Station", validators=[DataRequired()])
    upload_folder1 = FileField("Aldrino File:",validators=[DataRequired()])
    upload_folder2 = FileField("HV File:",validators=[DataRequired()])
    upload_folder3 = FileField("LV File:",validators=[DataRequired()])
    upload_folder4 = FileField("IV File:",validators=[DataRequired()])
    upload_folder5 = FileField("ROOT File:",validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit= SubmitField("Save")

# add two a table with 2 column 5 rows with module id field and add 4 root file



# ------------------------- Noise Test form End ------------------------------------>

