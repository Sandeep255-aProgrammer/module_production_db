from werkzeug.utils import secure_filename
import os
from database_table_new import (db , UserTable , DateTimeTable , StationTable , TempHumiDewTable ,MaterialReceivingCommonTable , SensorTable , FEHTable , SEHTable , MainBridgeTable , StumpBridgeTable ,
KaptonTapeTable , OtherTable , VTRxTable , GroundBalancerTable , GlueTable , WireBonderTable, VSensorTable, VFEHTable , VSEHTable,
VMainBridgeTable , VStumpBridgeTable , KaptonGluingTable , HVTable , IVTable , SensorGluingTable , NeedleMetrologyTable , SkeletonTestTable,
HybridGluingTable , ModuleEncapsulationTable , WireBondingTable , NoiseTest1Table , NoiseTest2Table , BurninTestTable )
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from database_table1 import (db , UserTable , DateTimeTable , StationTable , TempHumiDewTable ,MaterialReceivingCommonTable , SensorTable , FEHTable , SEHTable , MainBridgeTable , StumpBridgeTable ,
KaptonTapeTable , OtherTable , VTRxTable , GroundBalancerTable , GlueTable , WireBonderTable, VSensorTable, VFEHTable , VSEHTable,
VMainBridgeTable , VStumpBridgeTable , KaptonGluingTable , HVTable , IVTable , SensorGluingTable , NeedleMetrologyTable , SkeletonTestTable,
HybridGluingTable , ModuleEncapsulationTable , WireBondingTable , NoiseTest1Table , NoiseTest2Table , BurninTestTable )

class SaveFormToDataBase():
    def __init__(self,folder_url,db):
        self.folder_path = folder_url
    def save_file(self, file , file_name) -> str:
        """
        Save the uploaded file to the specified folder and return the file path.
        """
        if file:
            #filename = secure_filename(file.filename)
            # Ensure the directory exists
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            
            file_path = os.path.join(self.folder_path, file_name)
            file.save(file_path)
            return file_path
        return ''  # Return empty string if no file was uploaded
    def save_station(self, form , user_id) -> object:
        """
        Save a station form to the database using the provided station model.
        """
        try:
            station_data = {
                "station_name": form.station_name.data,
                "station_location": form.station_location.data,
                "remarks": form.station_remarks.data,
                "created_at": form.station_created_at.data,
                "img_path": self.save_file(form.station_img.data),  # Save image and get path
                "is_active": form.station_is_active.data,
                "iteration_number": form.station_iteration_number.data,
                "operator_id": user_id
            }

            # Add station to the database
            station_entry = StationTable.save_station(station_data)
            return station_entry  # Return the added station instance

        except Exception as e:
            self.db.session.rollback()
            flash(f"An error occurred while saving the station: {str(e)}", 'error')
            return None
    def save_VSensor(self,form: FlaskForm, user_id: int,file_name):
        """
        Saves the visual sensor inspection data to the database.

        Parameters:
        form (SensorVisualForm): The form containing the visual inspection data.
        user_id (int): The ID of the user performing the inspection.

        Returns:
        VSensorTable: The saved VSensorTable entry.

        Raises:
        ValueError: If validation fails or database constraints are violated.
        """
        station_data = {
    "station_name": "Station 1",
    "station_location": "Location A",
    "remarks": "Initial setup",
    "created_at": datetime.utcnow(),
    "img_path": "/images/station1.jpg",
    "is_active": True,
    "iteration_number": 1,
    "operator_id": 1  # Assume this user_id exists in the UserTable
}
        station_entry = StationTable.add_station(station_data)

        try:
            # Step 1: Save TempHumiDewTable entry
            temp_humi_dew_data = {
                "temperature": form.temp.data,
                "dew_point": form.dew_point.data,
                "humidity": form.humidity.data
            }
            temp_humi_dew_entry = TempHumiDewTable.add_temp_humi_dew(temp_humi_dew_data)

            # Step 2: Get SensorTable entry by matching sensor_id from the form
            # sensor_entry = SensorTable.query.filter_by(sensor_id=form.sensor_id.data).first()
            # if not sensor_entry:
                # raise ValueError(f"Sensor with ID {form.sensor_id.data} not found.")

            # Step 3: Map working_date to DateTimeTable
            # Assuming DateTimeTable has a field `date` and `id`
            working_date = form.working_date.data
            date_time_entry = DateTimeTable.query.filter_by(date_time=working_date).first()
            if not date_time_entry:
                date_time_data = {
        "date_time": datetime(2025, 1, 29, 17, 42, 19)
    }
                date_time_entry = DateTimeTable.add_date_time(date_time_data)
            
            # Step 4: Handle image upload (assuming you have a function to save the image)
            image_filename = self.save_file(form.image.data, file_name)  # Implement this function to save the image file

            # Step 5: Save VSensorTable entry
            v_sensor_data = {
                "date_time_id": date_time_entry.id,  # Use the DateTimeTable entry's ID
                "user_id": user_id,  # User ID from the session or form
                "sensor_id": 1,  # Sensor ID from the SensorTable entry
                "station_id": 1,  # Assuming station_id is provided or fetched
                "temp_humi_dewid": temp_humi_dew_entry.id,  # TempHumiDewTable entry's ID
                "image": image_filename,  # Save the image filename or path
                "comment": form.comment.data  # Comment from the form
            }

            v_sensor_entry = VSensorTable.add_v_sensor_entry(v_sensor_data)

            return v_sensor_entry  # Return the saved VSensorTable entry

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")
    def save_VFEH(self,form: FlaskForm, user_id: int):
        """
        Saves the visual FEH inspection data to the database.

        Parameters:
        form (FEHVisualForm): The form containing the visual inspection data.
        user_id (int): The ID of the user performing the inspection.

        Returns:
        VFEHTable: The saved VFEHTable entry.

        Raises:
        ValueError: If validation fails or database constraints are violated.
        """
        try:
            # Step 1: Save TempHumiDewTable entry
            temp_humi_dew_data = {
                "temperature": form.temp.data,
                "dew_point": form.dew_point.data,
                "humidity": form.humidity.data
            }
            temp_humi_dew_entry = TempHumiDewTable.add_temp_humi_dew(temp_humi_dew_data)

            # Step 2: Get FEHTable entry by matching FEH_id from the form
            feh_entry = FEHTable.query.filter_by(FEH_id=form.FEH_id.data).first()
            if not feh_entry:
                raise ValueError(f"FEH with ID {form.FEH_id.data} not found.")

            # Step 3: Map working_date to DateTimeTable
            # Assuming DateTimeTable has a field `date` and `id`
            working_date = form.working_date.data
            date_time_entry = DateTimeTable.query.filter_by(date=working_date).first()
            if not date_time_entry:
                # Create a new DateTimeTable entry if it doesn't exist
                date_time_entry = DateTimeTable(date=working_date)
                db.session.add(date_time_entry)
                db.session.commit()

            # Step 4: Handle image upload (assuming you have a function to save the image)
            image_filename = self.save_file(form.image.data)  # Implement this function to save the image file

            # Step 5: Save VFEHTable entry
            v_feh_data = {
                "datetime_id": date_time_entry.id,  # Use the DateTimeTable entry's ID
                "user_id": user_id,  # User ID from the session or form
                "feh_id": feh_entry.id,  # FEH ID from the FEHTable entry
                "station_id": 1,  # Assuming station_id is provided or fetched
                "temp_humi_dewid": temp_humi_dew_entry.id,  # TempHumiDewTable entry's ID
                "image": image_filename,  # Save the image filename or path
                "comment": form.comment.data  # Comment from the form
            }

            v_feh_entry = VFEHTable.add_v_feh_entry(v_feh_data)

            return v_feh_entry  # Return the saved VFEHTable entry

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")
    def save_VSEH(self,form: FlaskForm, user_id: int):
        """
        Saves the visual SEH inspection data to the database.

        Parameters:
        form (SEHVisualForm): The form containing the visual inspection data.
        user_id (int): The ID of the user performing the inspection.

        Returns:
        VSEHTable: The saved VSEHTable entry.

        Raises:
        ValueError: If validation fails or database constraints are violated.
        """
        try:
            # Step 1: Save TempHumiDewTable entry
            temp_humi_dew_data = {
                "temperature": form.temp.data,
                "dew_point": form.dew_point.data,
                "humidity": form.humidity.data
            }
            temp_humi_dew_entry = TempHumiDewTable.add_temp_humi_dew(temp_humi_dew_data)

            # Step 2: Get SEHTable entry by matching SEH_id from the form
            seh_entry = SEHTable.query.filter_by(SEH_id=form.SEH_id.data).first()
            if not seh_entry:
                raise ValueError(f"SEH with ID {form.SEH_id.data} not found.")

            # Step 3: Map working_date to DateTimeTable
            # Assuming DateTimeTable has a field `date` and `id`
            working_date = form.working_date.data
            date_time_entry = DateTimeTable.query.filter_by(date=working_date).first()
            if not date_time_entry:
                # Create a new DateTimeTable entry if it doesn't exist
                date_time_entry = DateTimeTable(date=working_date)
                db.session.add(date_time_entry)
                db.session.commit()

            # Step 4: Handle image upload (assuming you have a function to save the image)
            image_filename = self.save_file(form.image.data)  # Implement this function to save the image file

            # Step 5: Save VSEHTable entry
            v_seh_data = {
                "datetime_id": date_time_entry.id,  # Use the DateTimeTable entry's ID
                "user_id": user_id,  # User ID from the session or form
                "seh_id": seh_entry.id,  # SEH ID from the SEHTable entry
                "station_id": 1,  # Assuming station_id is provided or fetched
                "temp_humi_dewid": temp_humi_dew_entry.id,  # TempHumiDewTable entry's ID
                "image": image_filename,  # Save the image filename or path
                "comment": form.comment.data  # Comment from the form
            }

            v_seh_entry = VSEHTable.add_v_seh_entry(v_seh_data)

            return v_seh_entry  # Return the saved VSEHTable entry

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")
    def save_VMainBridge(self,form: FlaskForm, user_id: int):
        """
        Saves the visual Main Bridge inspection data to the database.

        Parameters:
        form (MainBridgeVisualForm): The form containing the visual inspection data.
        user_id (int): The ID of the user performing the inspection.

        Returns:
        VMainBridgeTable: The saved VMainBridgeTable entry.

        Raises:
        ValueError: If validation fails or database constraints are violated.
        """
        try:
            # Step 1: Save TempHumiDewTable entry
            temp_humi_dew_data = {
                "temperature": form.temp.data,
                "dew_point": form.dew_point.data,
                "humidity": form.humidity.data
            }
            temp_humi_dew_entry = TempHumiDewTable.add_temp_humi_dew(temp_humi_dew_data)

            # Step 2: Get MainBridgeTable entry by matching main_bridge_id from the form
            main_bridge_entry = MainBridgeTable.query.filter_by(main_bridge_id=form.main_bridge_id.data).first()
            if not main_bridge_entry:
                raise ValueError(f"Main Bridge with ID {form.main_bridge_id.data} not found.")

            # Step 3: Map working_date to DateTimeTable
            # Assuming DateTimeTable has a field `date` and `id`
            working_date = form.working_date.data
            date_time_entry = DateTimeTable.query.filter_by(date=working_date).first()
            if not date_time_entry:
                # Create a new DateTimeTable entry if it doesn't exist
                date_time_entry = DateTimeTable(date=working_date)
                db.session.add(date_time_entry)
                db.session.commit()

            # Step 4: Handle image upload (assuming you have a function to save the image)
            image_filename = self.save_file(form.image.data)  # Implement this function to save the image file

            # Step 5: Save VMainBridgeTable entry
            v_main_bridge_data = {
                "datetime_id": date_time_entry.id,  # Use the DateTimeTable entry's ID
                "user_id": user_id,  # User ID from the session or form
                "main_bridge_id": main_bridge_entry.id,  # Main Bridge ID from the MainBridgeTable entry
                "station_id": 1,  # Assuming station_id is provided or fetched
                "temp_humi_dewid": temp_humi_dew_entry.id,  # TempHumiDewTable entry's ID
                "image": image_filename,  # Save the image filename or path
                "comment": form.comment.data  # Comment from the form
            }

            v_main_bridge_entry = VMainBridgeTable.add_v_main_bridge_entry(v_main_bridge_data)

            return v_main_bridge_entry  # Return the saved VMainBridgeTable entry

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")
    def save_VStumpBridge(self,form: FlaskForm, user_id: int):
        """
        Saves the visual Stump Bridge inspection data to the database.

        Parameters:
        form (StumpBridgeVisualForm): The form containing the visual inspection data.
        user_id (int): The ID of the user performing the inspection.

        Returns:
        VStumpBridgeTable: The saved VStumpBridgeTable entry.

        Raises:
        ValueError: If validation fails or database constraints are violated.
        """
        try:
            # Step 1: Save TempHumiDewTable entry
            temp_humi_dew_data = {
                "temperature": form.temp.data,
                "dew_point": form.dew_point.data,
                "humidity": form.humidity.data
            }
            temp_humi_dew_entry = TempHumiDewTable.add_temp_humi_dew(temp_humi_dew_data)

            # Step 2: Get StumpBridgeTable entry by matching stump_bridge_id from the form
            stump_bridge_entry = StumpBridgeTable.query.filter_by(stump_bridge_id=form.stump_bridge_id.data).first()
            if not stump_bridge_entry:
                raise ValueError(f"Stump Bridge with ID {form.stump_bridge_id.data} not found.")

            # Step 3: Map working_date to DateTimeTable
            # Assuming DateTimeTable has a field `date` and `id`
            working_date = form.working_date.data
            date_time_entry = DateTimeTable.query.filter_by(date=working_date).first()
            if not date_time_entry:
                # Create a new DateTimeTable entry if it doesn't exist
                date_time_entry = DateTimeTable(date=working_date)
                db.session.add(date_time_entry)
                db.session.commit()

            # Step 4: Handle image upload (assuming you have a function to save the image)
            image_filename = self.save_file(form.image.data)  # Implement this function to save the image file

            # Step 5: Save VStumpBridgeTable entry
            v_stump_bridge_data = {
                "datetime_id": date_time_entry.id,  # Use the DateTimeTable entry's ID
                "user_id": user_id,  # User ID from the session or form
                "stumpbridge_id": stump_bridge_entry.id,  # Stump Bridge ID from the StumpBridgeTable entry
                "station_id": 1,  # Assuming station_id is provided or fetched
                "temp_humi_dewid": temp_humi_dew_entry.id,  # TempHumiDewTable entry's ID
                "image": image_filename,  # Save the image filename or path
                "comment": form.comment.data  # Comment from the form
            }

            v_stump_bridge_entry = VStumpBridgeTable.add_v_stump_bridge_entry(v_stump_bridge_data)

            return v_stump_bridge_entry  # Return the saved VStumpBridgeTable entry

        except ValueError as e:
            db.session.rollback()
            raise ValueError(f"Validation error: {str(e)}")
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")



            

