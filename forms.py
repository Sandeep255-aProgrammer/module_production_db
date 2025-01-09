from flask_wtf import FlaskForm
from wtforms import IntegerField ,StringField, SubmitField, PasswordField ,FileField ,DateField , BooleanField , SelectField,  DateTimeField,FormField, FloatField , FieldList
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



#Material receiver



class MaterialReceiver(FlaskForm):
    material_name = SelectField("Material Name", choices=[('sensor', 'Sensor'), ('hybrid', 'Hybrid'), ('bridge', 'Bridge'),('glue','Glue'),('kapton tapes','Kapton Tapes'), ('optical fibre','Optical Fibre') ,('other', 'Other Consumables')], validators=[DataRequired()])
    other_material_name = StringField("Other Material Name")
    date = DateField("Date", format='%Y-%m-%d')
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment= CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

# VisualInspectionForm done
class VisualInspection(FlaskForm):
    # Dropdown menu for selecting the item type
    item_type = SelectField(
        "Item Type",
        choices=[
            ('sensor', 'Sensor'),
            ('hybrid', 'Hybrid'),
            ('bridge', 'Bridge')
        ],
        validators=[DataRequired()]
    )
    check_id = StringField("Item ID", validators=[DataRequired()])
   # receiver_name = StringField("Receiver Name", validators=[DataRequired()])
   # shipment_info = StringField("Shipment Info", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# KaptonGluing

class KaptonGluing(FlaskForm):
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
    part_A_batch_no = StringField("Polytec 601 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = StringField("Polytec 601 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])
    main_bridge_type = SelectField(
        'Main Bridge Type',
        choices=[('Main Bridge 1', 'Main Bridge 1'), ('Main Bridge 2', 'Main Bridge 2')],
        validators=[DataRequired()]
    )
    main_bridge_id = StringField("Main Bridge ID", validators=[DataRequired()])
    
    # Stump bridge type and ID
    stump_bridge_type = SelectField(
        'Stump Bridge Type',
        choices=[('Stump Bridge 1', 'Stump Bridge 1'), ('Stump Bridge 2', 'Stump Bridge 2')],
        validators=[DataRequired()]
    )
    stump_bridge_id = StringField("Stump Bridge ID", validators=[DataRequired()])
    image = FileField("Upload Image (optional)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#date = DateField("Expary Date", format='%Y-%m-%d' ,validators=[DataRequired()])
# HV and IV Test

class HvIvForm(FlaskForm):
    sensor_id = SelectField("Sensor ID", validators=[DataRequired()])
    sensor_type = SelectField(
        'Sensor Type',
        choices=[('Top Sensor', 'Top Sensor'), ('Bottom Sensor', 'Bottom Sensor')],
        validators=[DataRequired()]
    )
    cooling_points = SelectField(
        'Cooling Point',
        choices=[('6 cp', '6 cp'), ('5 cp', '5 cp')],
        validators=[DataRequired()])
    hv_plot = FileField("HV Plot" ,validators=[DataRequired()])
    iv_plot =  FileField("IV Plot" ,validators=[DataRequired()])
  # upload csv
    csv_file = FileField("Upload Csv File")
    image = FileField("Upload Image(optional)")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#SensorGluing

class SensorGluing(FlaskForm):
    bare_module_id = StringField("Bare_Module ID/Name", validators=[DataRequired()])
    top_sensor_id = SelectField("Top Sensor ID", validators=[DataRequired()])
    bottom_sensor_id = SelectField("Bottom Sensor ID", validators=[DataRequired()])
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
    image = FileField("Upload Image")
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
#Needle Metrology

class NeedleMetrologyForm(FlaskForm):
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
    skeleton_id = StringField("Skeleton ID", validators=[DataRequired()])
    FEH_L =  StringField("FEH_LID", validators=[DataRequired()])
    FEH_R = StringField("FEH_RID", validators=[DataRequired()])
    VTRx = StringField("VTRx+_ID", validators=[DataRequired()])
    ground_balancer_id = StringField("Ground Balancer ID", validators=[DataRequired()])
# upload a root file 
    root_file = FileField("Upload File (root)" )
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")
# Hybrid Gluing

class HybridGluingForm(FlaskForm):
  # define the actual module id 
    module_id = SelectField("Module ID", validators=[DataRequired()])
    bare_module_id = SelectField("Bare_Module ID", validators=[DataRequired()])
    #top_sensor = StringField("Top Sensor ID", validators=[DataRequired()])
    #buttom_sensor = StringField("Bottom Sensor ID", validators=[DataRequired()])
    skeleton_id = SelectField("Skeleton ID", validators=[DataRequired()])
    part_A_batch_no = StringField("Polytec TC437 partA / Batch No :")
    part_A_exp_date = DateField("part A Expiry Date", format='%Y-%m-%d' ,validators=[DataRequired()])
    part_B_batch_no = StringField("Polytec TC437 partB / Batch No :")
    part_B_exp_date = DateField("part B Expiry Date", format='%Y-%m-%d', validators=[DataRequired()])

    image = FileField("Upload Image (optional)")
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
    # check_id = StringField("Check ID", validators=[DataRequired()])
    # receiver_name= StringField("Receiver Name ", validators=[DataRequired()])
    # shipment_info = StringField("Shipment Info ", validators=[DataRequired()])
    # Add the type of break dropdown menu with options
    type_of_break = SelectField(
        "Type of Break",
        choices=[
            ("", "Select"),  # Default option
            ("1", "1 - Wire cut"),
            ("2", "2 - Lift-off on sensor"),
            ("3", "3 - Heel break on sensor"),
            ("4", "4 - Lift-off on hybrid"),
            ("5", "5 - Heel break on hybrid"),
            ("0", "0 - Wire doesn't break"),
            ("6", "6 - Others"),
        ],
        validators=[DataRequired()],
    )
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Save")

#NoiseTest

class NoiseTestForm(FlaskForm):
    module_id = StringField("Module ID", validators=[DataRequired()])
    root_file = FileField("Upload Result (root file)" ,validators=[DataRequired()])
    image = FileField("Upload Image" ,validators=[DataRequired()])
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit= SubmitField("Save")
#BufNim Test

class BurNimForm(FlaskForm):
    module_quantity = SelectField(
    "Module Quantity",
    choices=[(str(i), str(i)) for i in range(1, 11)], 
    validators=[DataRequired()]
)
   
    submit = SubmitField("Go")


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












