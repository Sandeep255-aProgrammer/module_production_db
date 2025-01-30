from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import Form , DecimalField ,IntegerField ,StringField, SubmitField, PasswordField ,FileField ,DateField , BooleanField , SelectField,  DateTimeField,FormField, FloatField , FieldList
from wtforms.validators import DataRequired, URL, Optional
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

class WireBond(FlaskForm):
    # New Fields
    delta_height = DecimalField("ΔHEIGHT", validators=[DataRequired()])
    correction_factor_k1_sen = DecimalField("Correction Factor K1 (SEN)", validators=[DataRequired()])
    correction_factor_k2_feh = DecimalField("Correction Factor K2 (FEH)", validators=[DataRequired()])
    mean_force_1 = DecimalField("Mean Force 1 (g)", validators=[DataRequired()])
    mean_force_2 = DecimalField("Mean Force 2 (g)", validators=[DataRequired()])
    rms_value = DecimalField("RMS Value (%)", validators=[DataRequired()])
    standard_deviation = DecimalField("Standard Deviation", validators=[DataRequired()])
    
    # Additional Fields
    extra_files = FileField("Upload Additional Files (PDF, etc.)")
    comment = StringField("Comment", validators=[DataRequired()])
    module_id = StringField("Module ID", validators=[DataRequired()])
    
    # Add/Update selection
    action_type = SelectField("Action", choices=[('add', 'Add'), ('update', 'Update')], validators=[DataRequired()])
    
    submit = SubmitField("Submit")
class JigIDForm(FlaskForm):
    jig_id = FieldList(StringField("Jig ID", validators=[DataRequired()]), min_entries=1)

# List form for Sensor IDs
class SensorIdListForm(FlaskForm):
    Sensor_Ids = FieldList(StringField("Sensor ID", validators=[DataRequired()]), min_entries=1)

# List form for FEH IDs
class FEHIdListForm(FlaskForm):
    FEH_Ids = FieldList(StringField("FEH ID", validators=[DataRequired()]), min_entries=1)

# List form for SEH IDs
class SEHIdListForm(FlaskForm):
    SEH_Ids = FieldList(StringField("SEH ID", validators=[DataRequired()]), min_entries=1)

# List form for Main Bridge IDs
class MainBridgeIdListForm(FlaskForm):
    Main_Bridge_Ids = FieldList(StringField("Main Bridge ID", validators=[DataRequired()]), min_entries=1)

# List form for Stump Bridge IDs
class StumpBridgeIdListForm(FlaskForm):
    Stump_Bridge_Ids = FieldList(StringField("Stump Bridge ID", validators=[DataRequired()]), min_entries=1)

# List form for Glue Batch IDs
class Glue_id_exp(FlaskForm):
    Glue_Batch_Ids = StringField("Glue Batch ID", validators=[DataRequired()])
    Glue_Batch_Exp_Date = DateField("Glue Expiry Date",validators=[DataRequired()])

class GlueBatchIdListForm(FlaskForm):
    Glue_Batch = FieldList(FormField(Glue_id_exp), min_entries=1)
    
# List form for Kapton Tape IDs
class KaptonTapeIdListForm(FlaskForm):
    Kapton_Tape_Ids = FieldList(StringField("Kapton Tape ID", validators=[DataRequired()]), min_entries=1)

# List form for Optical Fibre IDs
class OpticalFibreIdListForm(FlaskForm):
    Optical_Fibre_Ids = FieldList(StringField("Optical Fibre ID", validators=[DataRequired()]), min_entries=1)

# List form for Wire Bonder Details
class WireBonderIds(FlaskForm):
    Spool_Numbers = StringField("Spool Number", validators=[DataRequired()])
    Wedge_Tools_No = StringField("Wedge Tool", validators=[DataRequired()])
    expiry_date = DateField("Wire Bond Expiry Date", validators=[DataRequired()])

class WireBonderDetailsForm(FlaskForm):
    Wire_Bonder_ids = FieldList(FormField(),min_entries=1)
# List form for Other Consumables
class OtherConsumablesListForm(FlaskForm):
    Other_Items = FieldList(StringField("Item Description", validators=[DataRequired()]), min_entries=1)




#Material receiver
class MaterialReceiverTypeForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()]); humidity = FloatField("Humidity", validators=[DataRequired()]); dew_point = FloatField("Dew Point", validators=[DataRequired()])
    material_type = SelectField('Item Type', choices=[('sensor', 'Sensor'), ('FEH', 'FEH'),("SEH","SEH"), ('main_bridge', 'Main Bridge'),("stump_bridge","Stump Bridge"),('glue','Glue'),('kapton_tapes','Kapton Tapes'), ('optical_fibre','Optical Fibre'),("wire_bonder","Wire Bonder") ,('other', 'Other Consumables')], validators=[DataRequired()])
    submit = SubmitField('Add')


class SensorForm(FlaskForm):
    recieved_from = StringField(validators=[DataRequired()])
    recieved_date = DateField(validators=[DataRequired()])
    #sensor_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    # uploads = MultipleFileField('Upload Files', validators=[FileAllowed(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])])
    sensor_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")    
    submit  = SubmitField('Add Sensor Ids')



# FEH Form
class FEHForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #feh_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    feh_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add FEH Ids')

# SEH Form
class SEHForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #seh_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    seh_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add SEH Ids')

# Main Bridge Form
class MainBridgeForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #main_bridge_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    main_bridge_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add Main Bridge Ids')

# Stump Bridge Form
class StumpBridgeForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #stump_bridge_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    stump_bridge_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add Stump Bridge Ids')

# Glue Form
class GlueForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #glue_batch_id = StringField(validators=[DataRequired()])
    #glue_exp_date = DateField(validators=[DataRequired()])
    glue_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField("Add glueId and expDate")
    #submit = SubmitField('Submit Glue')

# Kapton Tapes Form
class KaptonTapesForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #kapton_tape_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    kapton_tape_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add Kapton Tape Ids')

# Optical Fibre Form
class OpticalFibreForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #optical_fibre_id = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    optical_fibre_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add Optical Fibre Ids')

# Wire Bonder Form
class WireBonderForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    #spool_no= FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    #wedge_tool = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    #exp_date = DateField(validators=[DataRequired()])
    wire_bonder_img = FileField()
    Comment = CKEditorField("Comment")
    submit = SubmitField('Add spoolNo and wedgeTool')

# Other Consumables Form
class OtherConsumablesForm(FlaskForm):
    received_from = StringField(validators=[DataRequired()])
    received_date = DateField(validators=[DataRequired()])
    other_item_description = StringField(validators=[DataRequired()])
    other_item_img = FileField(validators=[DataRequired()])
    Comment = CKEditorField("Comment")
    submit = SubmitField('Submit Other Consumables')

class MaterialReceiver(FlaskForm):
    material_name = SelectField("Material Name", choices=[('sensor', 'Sensor'), ('FEH', 'FEH'),("SEH","SEH"), ('main_bridge', 'Main Bridge'),("stump_bridge","Stump Bridge"),('glue','Glue'),('kapton_tapes','Kapton Tapes'), ('optical fibre','Optical Fibre'),("wire_bonder","Wire Bonder") ,('other', 'Other Consumables')], validators=[DataRequired()])
    temp = FloatField("Temperature (°C)", validators=[DataRequired()]); humidity = FloatField("Humidity", validators=[DataRequired()]); dew_point = FloatField("Dew Point", validators=[DataRequired()])

    #temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    #humidity = FloatField("Humidity", validators=[DataRequired()])
    #dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    #material_name = SelectField("Material Name", choices=[('sensor', 'Sensor'), ('FEH', 'FEH'),("SEH","SEH"), ('main_bridge', 'Main Bridge'),("stump_bridge","Stump Bridge"),('glue','Glue'),('kapton_tapes','Kapton Tapes'), ('optical_fibre','Optical Fibre'),("wire_bonder","Wire Bonder") ], validators=[DataRequired()])
    other_material_name = StringField("Other Material Name")
    
    image = FileField("Upload Image" ,validators=[DataRequired()])# optional
    comment= CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

class AddJig(FlaskForm):
    jig_name_id = StringField("Jig No. ",validators=[DataRequired()])
    image = FileField("Upload Jig Image",validators=[DataRequired()])
    comment= CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# VisualInspectionForm done
class VisualInspection(FlaskForm):
    # Dropdown menu for selecting the item type
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    testfield_list = FieldList(StringField(),min_entries=1)
    item_type = SelectField(
        "Item Type",
        choices=[
            ('sensor', 'Sensor'),
            ('FEH', 'FEH'),
            ('SEH', 'SEH'),
            ('main_bridge','Main Bridge'),
            ('stump_bridge','Stump Bridge')
        ],
        validators=[DataRequired()]
    )
    check_id = StringField("Item ID", validators=[DataRequired()])
   # receiver_name = StringField("Receiver Name", validators=[DataRequired()])
   # shipment_info = StringField("Shipment Info", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()]) # compulsary 
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# KaptonGluing

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
    

    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    part_A_batch_no = SelectField("Polytec 601 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])# auto fill
    part_B_batch_no = SelectField("Polytec 601 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()]) # auto fill
    jig_no = SelectField("Select Jig No.",validators=[DataRequired()])
    image = FileField("Upload Image (optional)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#date = DateField("Expary Date", format='%Y-%m-%d' ,validators=[DataRequired()])
# HV and IV Test

class HvIvForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    sensor_id = SelectField("Sensor ID", validators=[DataRequired()])
    sensor_type = SelectField(
        'Sensor Type',
        choices=[('Top Sensor', 'Top Sensor'), ('Bottom Sensor', 'Bottom Sensor')],
        validators=[DataRequired()]
    ) #auto
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()])#auto
    hv_plot = FileField("HV Plot" ,validators=[DataRequired()])
    iv_plot =  FileField("IV Plot" ,validators=[DataRequired()])
  # upload csv
    csv_file = FileField("Upload Csv File")
    image = FileField("Upload Image(optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#SensorGluing

class SensorGluing(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    bare_module_id = StringField("Bare_Module ID/Name", validators=[DataRequired()])
    top_sensor_id = SelectField("Top Sensor ID", validators=[DataRequired()])
    bottom_sensor_id = SelectField("Bottom Sensor ID", validators=[DataRequired()])
    main_bridge = SelectField("Main Bridge ID", validators=[DataRequired()])
    stump_bridge = SelectField("Stump Bridge ID", validators=[DataRequired()])
    module_spacing =  SelectField("Module Spacing" ,choices=[('1.8mm' , '1.8mm')],validators=[DataRequired()])
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()]
    )
    jigs  = StringField("Jig No.", validators=[DataRequired()])
    part_A_batch_no = SelectField("Polytec TC437 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = SelectField("Polytec TC437 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()]) #auto
    image = FileField("Upload Image")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
#Needle Metrology

class NeedleMetrologyForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    bare_module_id = SelectField("Bare_Module ID", validators=[DataRequired()])
    x_coordinate = StringField("Delta x", validators=[DataRequired()])
    y_coordinate = StringField("Delta y", validators=[DataRequired()])
    del_theta = StringField("Rotation", validators=[DataRequired()])
    csv_xl = FileField("Upload Data (csv/excel)" ,validators=[DataRequired()])
    image = FileField("Upload Image (optional)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# Skeleton test

class SkeletonTestForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    skeleton_id = SelectField("Skeleton ID", validators=[DataRequired()])
    FEH_L =  SelectField("FEH_LID", validators=[DataRequired()])
    FEH_R = SelectField("FEH_RID", validators=[DataRequired()])
    SEH = SelectField("SEH",validators=[DataRequired()])
    VTRx = SelectField("VTRx+_ID", validators=[DataRequired()])
    ground_balancer_id = SelectField("Ground Balancer ID", validators=[DataRequired()])
# upload a root file 
    file = FileField("Upload Folder ",validators=[DataRequired()],render_kw={'webkitdirectory': True} )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# Hybrid Gluing

class HybridGluingForm(FlaskForm):
  # define the actual module id 
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = SelectField("Module ID", validators=[DataRequired()])
    bare_module_id = SelectField("Bare_Module ID", validators=[DataRequired()])
    #top_sensor = StringField("Top Sensor ID", validators=[DataRequired()])
    #buttom_sensor = StringField("Bottom Sensor ID", validators=[DataRequired()])
    skeleton_id = SelectField("Skeleton ID", validators=[DataRequired()])
    part_A_batch_no = SelectField("Polytec TC437 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = SelectField("Polytec TC437 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])

    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")


# Module inforamtion

class ModuleData(FlaskForm):
   # temp = FloatField("Temperature (°C)", validators=[DataRequired()])
   # humidity = FloatField("Humidity", validators=[DataRequired()])
   # dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_id = SelectField("Module_ID", validators=[DataRequired()])
    #FEH_L =  StringField("FEH_LID", validators=[DataRequired()])
    #FEH_R = StringField("FEH_RID", validators=[DataRequired()])
    #VTRx = StringField("VTRx+_ID", validators=[DataRequired()])
    #image = FileField("Upload Image")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
    
#Wire Bonding

class WireBondingForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    # check_id = StringField("Check ID", validators=[DataRequired()])
    # receiver_name= StringField("Receiver Name ", validators=[DataRequired()])
    # shipment_info = StringField("Shipment Info ", validators=[DataRequired()])
    # Add the type of break dropdown menu with options
    #type_of_break = SelectField(
       
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#NoiseTest
class NoiseTestForm_Ph2_ACF(FlaskForm):
    temp = FloatField("Temperature (°C):", validators=[DataRequired()])
    humidity = FloatField("Humidity:", validators=[DataRequired()])
    dew_point = FloatField("Dew Point:", validators=[DataRequired()])
    working_date = DateField("Working Date:", validators=[DataRequired()])
    module_id = SelectField("Module ID:",validators=[DataRequired()])
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
    upload_folder1 = FileField("Aldrino File:",validators=[DataRequired()])
    upload_folder2 = FileField("HV File:",validators=[DataRequired()])
    upload_folder3 = FileField("LV File:",validators=[DataRequired()])
    upload_folder4 = FileField("IV File:",validators=[DataRequired()])
    upload_folder5 = FileField("ROOT File:",validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit= SubmitField("Save")

#Burnin Test
# add two a table with 2 column 5 rows with module id field and add 4 root file
class BurninForm(FlaskForm):
    temp = FloatField("Temperature (°C)", validators=[DataRequired()])
    humidity = FloatField("Humidity", validators=[DataRequired()])
    dew_point = FloatField("Dew Point", validators=[DataRequired()])
    working_date = DateField("Working Date", validators=[DataRequired()])
    module_quantity = SelectField(
    "Module Quantity",
    choices=[(str(i), str(i)) for i in range(1, 11)], 
    validators=[DataRequired()]
)
    submit = SubmitField("Save")


class BurnimForm1(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm1, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm2(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm2, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm3(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm3, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm4(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm4, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm5(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm5, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm6(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    module6_id = SelectField("Sixth Module ID", validators=[DataRequired()])
    module6_result = FileField("Upload Sixth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm6, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module6_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm7(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    module6_id = SelectField("Sixth Module ID", validators=[DataRequired()])
    module6_result = FileField("Upload Sixth Module Result (root)", validators=[DataRequired()])
    module7_id = SelectField("Seventh Module ID", validators=[DataRequired()])
    module7_result = FileField("Upload Seventh Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm7, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module6_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module7_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm8(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    module6_id = SelectField("Sixth Module ID", validators=[DataRequired()])
    module6_result = FileField("Upload Sixth Module Result (root)", validators=[DataRequired()])
    module7_id = SelectField("Seventh Module ID", validators=[DataRequired()])
    module7_result = FileField("Upload Seventh Module Result (root)", validators=[DataRequired()])
    module8_id = SelectField("Eighth Module ID", validators=[DataRequired()])
    module8_result = FileField("Upload Eighth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm8, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module6_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module7_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module8_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm9(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    module6_id = SelectField("Sixth Module ID", validators=[DataRequired()])
    module6_result = FileField("Upload Sixth Module Result (root)", validators=[DataRequired()])
    module7_id = SelectField("Seventh Module ID", validators=[DataRequired()])
    module7_result = FileField("Upload Seventh Module Result (root)", validators=[DataRequired()])
    module8_id = SelectField("Eighth Module ID", validators=[DataRequired()])
    module8_result = FileField("Upload Eighth Module Result (root)", validators=[DataRequired()])
    module9_id = SelectField("Ninth Module ID", validators=[DataRequired()])
    module9_result = FileField("Upload Ninth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm9, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module6_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module7_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module8_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module9_id.choices = [(module_id, module_id) for module_id, in module_ids]


class BurnimForm10(FlaskForm):
    module1_id = SelectField("First Module ID", validators=[DataRequired()])
    module1_result = FileField("Upload First Module Result (root)", validators=[DataRequired()])
    module2_id = SelectField("Second Module ID", validators=[DataRequired()])
    module2_result = FileField("Upload Second Module Result (root)", validators=[DataRequired()])
    module3_id = SelectField("Third Module ID", validators=[DataRequired()])
    module3_result = FileField("Upload Third Module Result (root)", validators=[DataRequired()])
    module4_id = SelectField("Fourth Module ID", validators=[DataRequired()])
    module4_result = FileField("Upload Fourth Module Result (root)", validators=[DataRequired()])
    module5_id = SelectField("Fifth Module ID", validators=[DataRequired()])
    module5_result = FileField("Upload Fifth Module Result (root)", validators=[DataRequired()])
    module6_id = SelectField("Sixth Module ID", validators=[DataRequired()])
    module6_result = FileField("Upload Sixth Module Result (root)", validators=[DataRequired()])
    module7_id = SelectField("Seventh Module ID", validators=[DataRequired()])
    module7_result = FileField("Upload Seventh Module Result (root)", validators=[DataRequired()])
    module8_id = SelectField("Eighth Module ID", validators=[DataRequired()])
    module8_result = FileField("Upload Eighth Module Result (root)", validators=[DataRequired()])
    module9_id = SelectField("Ninth Module ID", validators=[DataRequired()])
    module9_result = FileField("Upload Ninth Module Result (root)", validators=[DataRequired()])
    module10_id = SelectField("Tenth Module ID", validators=[DataRequired()])
    module10_result = FileField("Upload Tenth Module Result (root)", validators=[DataRequired()])
    burnim_box_result = FileField("Upload Burnim Box Result (root)", validators=[DataRequired()])
    image = FileField("Upload Image (optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, module_ids, *args, **kwargs):
        super(BurnimForm10, self).__init__(*args, **kwargs)
        # Set the choices for the SelectField dynamically
        self.module1_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module2_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module3_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module4_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module5_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module6_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module7_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module8_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module9_id.choices = [(module_id, module_id) for module_id, in module_ids]
        self.module10_id.choices = [(module_id, module_id) for module_id, in module_ids]












