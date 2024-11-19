from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField ,FileField ,DateField , BooleanField , SelectField,  DateTimeField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField



'''
This is the py file for making forms , it is based on wtforms module so visit the website to learn more about this module like fields , FileField etc 


'''






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


# create Station Add forms
class AddStationForm(FlaskForm):
    station_name = StringField("Station Name", validators=[DataRequired()])
    station_img = FileField("Upload the Station Image", validators=[DataRequired()])
    station_remarks = CKEditorField("Remarks", validators=[DataRequired()])
    station_created_at = DateTimeField("Created At", format='%Y-%m-%d %H:%M:%S')
    station_location = StringField("Station Location", validators=[DataRequired()])
    station_is_active = BooleanField("Is station active in this status")
    station_operator = StringField("Operator", validators=[DataRequired()])
    station_iteration_number = StringField("Iteration Number", validators=[DataRequired()])
    submit= SubmitField("Save Station")

    # Link to the User table via the `username` field
    #operator: Mapped[str] = mapped_column(String(100), ForeignKey("Users.username"), nullable=False)



#Material reception
class MaterialReceiver(FlaskForm):
    material_name = StringField("Material_Name", validators=[DataRequired()])
    receiver_name = StringField("Receiver_Name", validators=[DataRequired()])
    date = DateField("Date", format='%Y-%m-%d')
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment= CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# VisualInspectionForm done

class VisualInspection(FlaskForm):
    check_id = StringField("Sensor ID", validators=[DataRequired()])
    receiver_name= StringField("Receiver Name ", validators=[DataRequired()])
    shipment_info = StringField("Shipment Info ", validators=[DataRequired()])
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment= CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# KaptonGluing

class KaptonGluing(FlaskForm):
    check_id = StringField("Sensor ID", validators=[DataRequired()])
    sensor_type = SelectField(
        'Sensor Type',
        choices=[('Top Sensor', 'Top Sensor'), ('Bottom Sensor', 'Bottom Sensor')],
        validators=[DataRequired()]
    )
    date = DateField("Expary Date", format='%Y-%m-%d')

    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    part_A_batch_no = StringField("Polytec 601 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = StringField("Polytec 601 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#date = DateField("Expary Date", format='%Y-%m-%d' ,validators=[DataRequired()])
# HV and IV Test

class HvIvForm(FlaskForm):
    check_id = StringField("Sensor ID", validators=[DataRequired()])
    sensor_type = SelectField(
        'Sensor Type',
        choices=[('Top Sensor', 'Top Sensor'), ('Bottom Sensor', 'Bottom Sensor')],
        validators=[DataRequired()]
    )
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()])
    hv_plots = FileField("HV Plot" ,validators=[DataRequired()])
    iv_plots =  FileField("IV Plot" ,validators=[DataRequired()])
  # upload csv
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#SensorGluing

class SensorGluing(FlaskForm):
    check_id = StringField("Bare_Module ID/Name", validators=[DataRequired()])
    top_sensor = StringField("Top Sensor ID", validators=[DataRequired()])
    buttom_sensor = StringField("Bottom Sensor ID", validators=[DataRequired()])
    #date = DateField("Expary Date", format='%Y-%m-%d')
    main_bridge = StringField("Main Bridge ID", validators=[DataRequired()])
    stump_bridge = StringField("Stump Bridge ID", validators=[DataRequired()])
    module_spacing =  SelectField("Module Spacing" ,choices=[('1.8mm' , '1.8mm')],validators=[DataRequired()])
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    jigs  = StringField("Jig No.", validators=[DataRequired()])
    part_A_batch_no = StringField("Polytec TC437 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = StringField("Polytec TC437 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
#Needle Metrology

class NeedleMetrologyForm(FlaskForm):
    check_id = StringField("Module No.", validators=[DataRequired()])
    x_coordinate = StringField("Delta x", validators=[DataRequired()])
    y_coordinate = StringField("Delta y", validators=[DataRequired()])
    del_theta = StringField("Rotation", validators=[DataRequired()])
    csv_xl = FileField("Upload Data (csv/excel)" ,validators=[DataRequired()])
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# Skeleton test

class SkeletonTestForm(FlaskForm):
    check_id = StringField("Skeleton ID", validators=[DataRequired()])
    FEH_L =  StringField("FEH_LID", validators=[DataRequired()])
    FEH_R = StringField("FEH_RID", validators=[DataRequired()])
    VTRx = StringField("VTRx+_ID", validators=[DataRequired()])
    Skeleton_ID = StringField("Ground Balancer ID", validators=[DataRequired()])
# upload a root file 
    image = FileField("Upload Image" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# Hybrid Gluing

class HybridGluingForm(FlaskForm):
  # define the actual module id 
    check_id = StringField("Module ID", validators=[DataRequired()])
    bare_module_id = StringField("Bare_Module ID", validators=[DataRequired()])
    #top_sensor = StringField("Top Sensor ID", validators=[DataRequired()])
    #buttom_sensor = StringField("Bottom Sensor ID", validators=[DataRequired()])
    skeleton_id = StringField("Skeleton ID", validators=[DataRequired()])
    part_A_batch_no = StringField("Polytec TC437 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = StringField("Polytec TC437 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])

    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")


# Module inforamtion

class ModuleData(FlaskForm):
    module_id = StringField("Module_ID", validators=[DataRequired()])
    #FEH_L =  StringField("FEH_LID", validators=[DataRequired()])
    #FEH_R = StringField("FEH_RID", validators=[DataRequired()])
    #VTRx = StringField("VTRx+_ID", validators=[DataRequired()])
    #image = FileField("Upload Image")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
#Wire Bonding

class WireBondingForm(FlaskForm):
    module_id = StringField("Module ID", validators=[DataRequired()])
    pull_test_result = StringField("Pull Test Result (gram)", validators=[DataRequired()]) # takes number
    
    
    image = FileField("Upload Image/Data" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#NoiseTest

class NoiseTestForm(FlaskForm):
    check_id = StringField("Module ID", validators=[DataRequired()])
    root_file = FileField("Upload Result (root file)" ,validators=[DataRequired()])
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit= SubmitField("Save")
#BufNim Test

class BurNimForm(FlaskForm):
    check_id = StringField("Module ID", validators=[DataRequired()]) # select multiple Module
    # result corresponding to each module and a overall root file (burnin box) 
    #image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
