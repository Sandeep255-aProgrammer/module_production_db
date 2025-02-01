from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Boolean, DateTime , Text , Float ,Date , Enum
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
import os
from sqlalchemy.exc import IntegrityError
import datetime
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# for each table add one extra field (for foreign key )
# --------------------- Authentication part -----------------------------------
# There are some unique field requirements in some database tables so later add something 
#so that it check it then return something without giving any error.
class UserTable(UserMixin, db.Model):
    __tablename__ = "UserTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)  
    # ---------------------------- Fields ------------------------------
    username: Mapped[str] = mapped_column(String(100), unique=True)  # Username as a unique field
    password: Mapped[str] = mapped_column(String(100))           # Password field
    name: Mapped[str] = mapped_column(String(100))              # Name field
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)  # Timestamp
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Boolean field for active status
    # --------------------------- Child Tables --------------------------------------
    station = relationship("StationTable", back_populates="user" )
    jig = relationship("JigTable", back_populates="user" )
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="user" )
    v_sensor = relationship("VSensorTable", back_populates="user" )
    v_feh = relationship("VFEHTable", back_populates="user" )
    v_seh = relationship("VSEHTable", back_populates="user" )
    v_main_bridge = relationship("VMainBridgeTable", back_populates="user" )
    v_stump_bridge = relationship("VStumpBridgeTable", back_populates="user" )
    kapton_gluing = relationship("KaptonGluingTable", back_populates="user" )
    hv = relationship("HVTable", back_populates="user" )
    iv = relationship("IVTable", back_populates="user" )
    sensor_gluing = relationship("SensorGluingTable", back_populates="user" )
    needle_metrology = relationship("NeedleMetrologyTable", back_populates="user" )
    skeleton_test = relationship("SkeletonTestTable", back_populates="user" )
    hybrid_gluing = relationship("HybridGluingTable", back_populates="user" )
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="user" )
    wire_bonding = relationship("WireBondingTable", back_populates="user" )
    noise_test1 = relationship("NoiseTest1Table", back_populates="user" )
    noise_test2 = relationship("NoiseTest2Table", back_populates="user" )
    burnin_test = relationship("BurninTestTable", back_populates="user" )
class DateTimeTable(db.Model):
    __tablename__ = "DateTimeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    # --------------------------Fields------------------------------------------------ 
    working_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    current_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    # ------------------------- Child Tables ------------------------------------------
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="date_time" )
    v_sensor = relationship("VSensorTable", back_populates="date_time" )
    v_feh = relationship("VFEHTable", back_populates="date_time" )
    v_seh = relationship("VSEHTable", back_populates="date_time" )
    v_main_bridge = relationship("VMainBridgeTable", back_populates="date_time" )
    v_stump_bridge = relationship("VStumpBridgeTable", back_populates="date_time" )
    kapton_gluing = relationship("KaptonGluingTable", back_populates="date_time" )
    hv = relationship("HVTable", back_populates="date_time" )
    iv = relationship("IVTable", back_populates="date_time" )
    sensor_gluing = relationship("SensorGluingTable", back_populates="date_time" )
    needle_metrology = relationship("NeedleMetrologyTable", back_populates="date_time" )
    skeleton_test = relationship("SkeletonTestTable", back_populates="date_time" )
    hybrid_gluing = relationship("HybridGluingTable", back_populates="date_time" )
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="date_time" )
    wire_bonding = relationship("WireBondingTable", back_populates="date_time" )
    noise_test1 = relationship("NoiseTest1Table", back_populates="date_time" )
    noise_test2 = relationship("NoiseTest2Table", back_populates="date_time" )
    burnin_test = relationship("BurninTestTable", back_populates="date_time" )

class StationTable(db.Model):
    __tablename__ = "StationTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ------------------------------- Fields ---------------------------
    station_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    station_location: Mapped[str] = mapped_column(String(100), nullable=False)
    remarks: Mapped[str] = mapped_column(String(4000))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow, nullable=False)  # Timestamp
    img_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Boolean field for active status
    iteration_number: Mapped[int] = mapped_column(Integer, nullable=False)
    # ----------------------------- Parent Table ---------------------------------
    operator_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="station")
    # ----------------------------- Child Tables ----------------------------------
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="station")
    v_sensor = relationship("VSensorTable", back_populates="station")
    v_feh = relationship("VFEHTable", back_populates="station")
    v_seh = relationship("VSEHTable", back_populates="station")
    v_main_bridge = relationship("VMainBridgeTable", back_populates="station")
    v_stump_bridge = relationship("VStumpBridgeTable", back_populates="station")
    kapton_gluing = relationship("KaptonGluingTable", back_populates="station")
    hv = relationship("HVTable", back_populates="station")
    iv = relationship("IVTable", back_populates="station")
    sensor_gluing = relationship("SensorGluingTable", back_populates="station")
    needle_metrology = relationship("NeedleMetrologyTable", back_populates="station")
    skeleton_test = relationship("SkeletonTestTable", back_populates="station")
    hybrid_gluing = relationship("HybridGluingTable", back_populates="station")
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="station")
    wire_bonding = relationship("WireBondingTable", back_populates="station")
    noise_test1 = relationship("NoiseTest1Table", back_populates="station")
    noise_test2 = relationship("NoiseTest2Table", back_populates="station")
    burnin_test = relationship("BurninTestTable", back_populates="station")
    
# --------------------------- Basic Form ---------------------------------------------!

class TempHumiDewTable(db.Model):
    __tablename__ = "TempHumiDewTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Fields
    temperature: Mapped[float] = mapped_column(Float, nullable=False)  
    dew_point: Mapped[float] = mapped_column(Float, nullable=False)   
    humidity: Mapped[float] = mapped_column(Float, nullable=False)    
    # ------------------------------- Parent Tables -------------------------
    # -------------------------------- Child Tables --------------------------
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="temp_humi_dew")
    hybrid_gluing = relationship("HybridGluingTable", back_populates="temp_humi_dew")
    sensor_gluing = relationship("SensorGluingTable", back_populates="temp_humi_dew")
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="temp_humi_dew")
    wire_bonding = relationship("WireBondingTable", back_populates="temp_humi_dew")
    noise_test1 = relationship("NoiseTest1Table", back_populates="temp_humi_dew")
    noise_test2 = relationship("NoiseTest2Table", back_populates="temp_humi_dew")
    burnin_test = relationship("BurninTestTable", back_populates="temp_humi_dew")
    needle_metrology = relationship("NeedleMetrologyTable", back_populates="temp_humi_dew")
    skeleton_test = relationship("SkeletonTestTable", back_populates="temp_humi_dew")
    hv = relationship("HVTable", back_populates="temp_humi_dew")
    iv = relationship("IVTable", back_populates="temp_humi_dew")
    v_sensor = relationship("VSensorTable", back_populates="temp_humi_dew" )
    v_feh = relationship("VFEHTable", back_populates="temp_humi_dew" )
    v_seh = relationship("VSEHTable", back_populates="temp_humi_dew" )
    v_main_bridge = relationship("VMainBridgeTable", back_populates="temp_humi_dew" )
    kapton_gluing = relationship("KaptonGluingTable", back_populates="temp_humi_dew")
    v_stump_bridge = relationship("VStumpBridgeTable", back_populates="temp_humi_dew" )
    
# ----------------  All tables linked to Material Receiver _--------------------------!
# ---- will be refered to the material table -----------------
# material id , 
class MaterialReceivingCommonTable(db.Model):
    __tablename__ = "MaterialReceivingCommonTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # Fields
    received_from: Mapped[str] = mapped_column(String(255), nullable=False)  # Who the material was received from
    received_date:Mapped[datetime.date] = mapped_column(Date, nullable=False)
    material_name: Mapped[str] = mapped_column(String(255), nullable=False)  # Name of the material
    img: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image path
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments
    #  ------------------------------- Parent Tables ---------------------------------

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)  # Link to User table
    user = relationship("UserTable", back_populates="material_receiver_common")
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)  # Link to DateTime table
    date_time = relationship("DateTimeTable", back_populates="material_receiver_common")
    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)  # Link to TempHumiDew table
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="material_receiver_common")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="material_receiver_common")
    # ------------------------------- Child Tables ------------------------------------
    sensor = relationship("SensorTable", back_populates="material_receiver_common" )
    feh = relationship("FEHTable", back_populates="material_receiver_common" )
    seh = relationship("SEHTable", back_populates="material_receiver_common" )
    main_bridge = relationship("MainBridgeTable", back_populates="material_receiver_common" )
    stump_bridge = relationship("StumpBridgeTable", back_populates="material_receiver_common" )
    kapton_tape = relationship("KaptonTapeTable", back_populates="material_receiver_common" )
    ground_balancer = relationship("GroundBalancerTable", back_populates="material_receiver_common" )
    vtrx = relationship("VTRxTable", back_populates="material_receiver_common" )
    glue = relationship("GlueTable", back_populates="material_receiver_common" )
    wire_bonder = relationship("WireBonderTable", back_populates="material_receiver_common" )
    other = relationship("OtherTable", back_populates="material_receiver_common" )
    jig = relationship("JigTable", back_populates="material_receiver_common" )
   

#---------------------------------------------------------------------------------------
# ----------------------------- Material Table -------------------
# foreign key : Module , Visual table , temp_humi_dew , Datetime , matreccomm., bareModule id and Skeleton test id 
class JigTable(db.Model):
    __tablename__ = 'JigTable'
    
    # fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="jig")
    # Define relationships to child tables
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="jig")
    skeleton_test = relationship("SkeletonTestTable", back_populates="jig")
    hybrid_gluing = relationship("HybridGluingTable", back_populates="jig")
    wire_bonding = relationship("WireBondingTable", back_populates="jig")
    sensor_gluing = relationship("SensorGluingTable", back_populates="jig")
    needle_metrology= relationship("NeedleMetrologyTable", back_populates="jig")
    kapton_gluing = relationship("KaptonGluingTable", back_populates="jig")
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="jig")
    
class SensorTable(db.Model):
    __tablename__ = "SensorTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # Fields
    sensor_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Type of the sensor
    sensor_type:Mapped[str] = mapped_column(String(255), nullable=True)
    # -------------------------- Child Tables --------------------------------
    kapton_gluing = relationship("KaptonGluingTable", back_populates="sensor" )
    hv = relationship("HVTable", back_populates="sensor" )
    iv = relationship("IVTable", back_populates="sensor" )
    sensor_gluing = relationship("SensorGluingTable", back_populates="sensor")
    v_sensor = relationship("VSensorTable", back_populates="sensor" )
    # ----------------------------- Parent Tables ------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="sensor")
    
class FEHTable(db.Model):
    __tablename__ = "FEHTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    feh_id: Mapped[str] = mapped_column(String(255), nullable=False) 
    feh_type:  Mapped[str] = mapped_column(String(255), nullable= True)
    # -----------------------------------  Child Tables ------------------------------
    v_feh = relationship("VFEHTable", back_populates="feh" )
    skeleton_test = relationship("SkeletonTestTable", back_populates="feh" )
    # ----------------------------------- Parent Tables -----------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="feh")
   

class SEHTable(db.Model):
    __tablename__ = "SEHTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    seh_id: Mapped[str] = mapped_column(String(255), nullable=False) 
    # ----------------------------- Child Tables ----------------------------------
    v_seh = relationship("VSEHTable", back_populates="seh" )
    skeleton_test = relationship("SkeletonTestTable", back_populates="seh" )
    # ---------------------------- Parent Tables -----------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="seh")
    

class MainBridgeTable(db.Model):
    __tablename__ = "MainBridgeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    main_bridge_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Name of the main bridge
    # ------------------------------- child Tables -----------------------------------
    sensor_gluing = relationship("SensorGluingTable", back_populates="main_bridge" )
    v_main_bridge = relationship("VMainBridgeTable", back_populates="main_bridge" )
    # ------------------------------- Parent Tables ------------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="main_bridge")
    
class StumpBridgeTable(db.Model):
    __tablename__ = "StumpBridgeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # Fields 
    stump_bridge_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Name of the stump bridge
    # ------------------------------- child tables ---------------------------------
    sensor_gluing = relationship("SensorGluingTable", back_populates="stump_bridge" )
    v_stump_bridge = relationship("VStumpBridgeTable", back_populates="stump_bridge" )
    # ------------------------------- Parent Tables --------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="stump_bridge")
    @classmethod
    def add_stump_bridge_entry(cls, stump_bridge_data: dict):
        """
        Adds a new Stump Bridge entry to the database.
        
        Parameters:
        stump_bridge_data (dict): A dictionary containing keys that match the columns of the StumpBridgeTable.

        Returns:
        StumpBridgeTable instance of the added entry.
        """
        try:
            # Ensure the required keys are provided in stump_bridge_data
            required_fields = {"stump_bridge_id", "material_receiver_common_id"}
            missing_fields = required_fields - stump_bridge_data.keys()
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            stump_bridge_entry = cls(**stump_bridge_data)
            db.session.add(stump_bridge_entry)
            db.session.commit()
            return stump_bridge_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class KaptonTapeTable(db.Model):
    __tablename__ = "KaptonTapeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    kapton_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Type of Kapton tape
    # ----------------------------------- parent tables ------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="kapton_tape")
    @classmethod
    def add_kapton_tape_entry(cls, kapton_tape_data: dict):
        """
        Adds a new Kapton Tape entry to the database.
        
        Parameters:
        kapton_tape_data (dict): A dictionary containing keys that match the columns of the KaptonTapeTable.

        Returns:
        KaptonTapeTable instance of the added entry.
        """
        try:
            # Ensure the required keys are provided in kapton_tape_data
            required_fields = {"kapton_id", "material_receiver_common_id"}
            missing_fields = required_fields - kapton_tape_data.keys()
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            kapton_tape_entry = cls(**kapton_tape_data)
            db.session.add(kapton_tape_entry)
            db.session.commit()
            return kapton_tape_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

   
class OtherTable(db.Model):
    __tablename__ = "OtherTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    material_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Description of the item
    # -------------------------------------- parent tables ------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="other")
    
class VTRxTable(db.Model):
    __tablename__ = "VTRxTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields ------------------
    vt_rx_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Name of the VTRx
    # ----------------------------- child tables -----------------------------------
    skeleton_test = relationship("SkeletonTestTable", back_populates="vtrx" )
    # ------------------------------ Parent Tables ----------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="vtrx")
    
class GroundBalancerTable(db.Model):
    __tablename__ = "GroundBalancerTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    ground_balancer_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Type of ground balancer
    # ---------------------------- child tables ---------------------------------
    skeleton_test = relationship("SkeletonTestTable", back_populates="ground_balancer" )
    # ----------------------------  parent tables -------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="ground_balancer")
    

class GlueTable(db.Model):
    __tablename__ = "GlueTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    glue_batch_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Glue batch id
    expiry_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)  # Expiry date of the glue
    # ------------------------------ child tables ---------------------------------
    sensor_gluing = relationship("SensorGluingTable", back_populates="glue" )
    kapton_gluing = relationship("KaptonGluingTable", back_populates="glue" )
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="glue" )
    hybrid_gluing = relationship("HybridGluingTable", back_populates="glue" )
    # ----------------------------------- parent tables ----------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="glue")
    @classmethod
    def add_glue_entry(cls, glue_data: dict):
        """
        Adds a new Glue entry to the database.

        Parameters:
        glue_data (dict): A dictionary containing keys that match the columns of the GlueTable.

        Returns:
        GlueTable instance of the added entry.
        """
        try:
            # Ensure the required keys are provided in glue_data
            required_fields = {"glue_batch_id", "expiry_date", "material_receiver_common_id"}
            missing_fields = required_fields - glue_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            glue_entry = cls(**glue_data)
            db.session.add(glue_entry)
            db.session.commit()
            return glue_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class WireBonderTable(db.Model):
    __tablename__ = "WireBonderTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    spool_no: Mapped[str] = mapped_column(String(255), nullable=False)  # Spool number for wire bonding
    wedge_no: Mapped[str] = mapped_column(String(255), nullable=False)  # Wedge number for wire bonding
    expiry_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)  # Expiry date of the wire bond material
    # -------------------- Parent Tables --------------------------------
    material_receiver_common_id: Mapped[int] = mapped_column(ForeignKey("MaterialReceivingCommonTable.id"), nullable=False)
    material_receiver_common = relationship("MaterialReceivingCommonTable", back_populates="wire_bonder")
    @classmethod
    def add_wire_bonder_entry(cls, wire_bonder_data: dict):
        """
        Adds a new Wire Bonder entry to the database.

        Parameters:
        wire_bonder_data (dict): A dictionary containing keys that match the columns of the WireBonderTable.

        Returns:
        WireBonderTable instance of the added entry.
        """
        try:
            # Ensure the required keys are provided in wire_bonder_data
            required_fields = {"spool_no", "wedge_no", "expiry_date", "material_receiver_common_id"}
            missing_fields = required_fields - wire_bonder_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            wire_bonder_entry = cls(**wire_bonder_data)
            db.session.add(wire_bonder_entry)
            db.session.commit()
            return wire_bonder_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

    
   
# ---------------------- Visual Inspection Tables ----------------------------
# foreign key : temp_humi_dew , Datetime , Material Table , Station id ,

class VSensorTable(db.Model):
    __tablename__ = "VSensorTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # Fields -------------------------------
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image of the visual inspection result
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments or notes
    # --------------------------- Parent Tables -------------------------------
    date_time_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="v_sensor")
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="v_sensor")
    sensor_id: Mapped[int] = mapped_column(ForeignKey("SensorTable.id"), nullable=False)  # Foreign key to SensorTable
    sensor = relationship("SensorTable", back_populates="v_sensor")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="v_sensor")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="v_sensor")
    @classmethod
    def add_v_sensor_entry(cls, v_sensor_data: dict):
        """
        Adds a new VSensor entry to the database.

        Parameters:
        v_sensor_data (dict): A dictionary containing the fields required for a VSensorTable entry.

        Returns:
        VSensorTable instance of the added entry.
        """
        try:
            # Ensure the required fields are present in v_sensor_data
            required_fields = {"date_time_id", "user_id", "sensor_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - v_sensor_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            v_sensor_entry = cls(**v_sensor_data)
            db.session.add(v_sensor_entry)
            db.session.commit()
            return v_sensor_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class VFEHTable(db.Model):
    __tablename__ = "VFEHTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image of the visual inspection result
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments or notes
    # --------------------------------- Parent Tables --------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)  
    date_time = relationship("DateTimeTable", back_populates="v_feh")
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="v_feh")
    feh_id: Mapped[int] = mapped_column(ForeignKey("FEHTable.id"), nullable=False)
    feh = relationship("FEHTable", back_populates="v_feh")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="v_feh")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="v_feh")
    @classmethod
    def add_v_feh_entry(cls, v_feh_data: dict):
        """
        Adds a new VFEH entry to the database.

        Parameters:
        v_feh_data (dict): A dictionary containing the fields required for a VFEHTable entry.

        Returns:
        VFEHTable instance of the added entry.
        """
        try:
            # Ensure the required fields are present in v_feh_data
            required_fields = {"datetime_id", "user_id", "feh_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - v_feh_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            v_feh_entry = cls(**v_feh_data)
            db.session.add(v_feh_entry)
            db.session.commit()
            return v_feh_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class VSEHTable(db.Model):
    __tablename__ = "VSEHTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields ------------
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image of the visual inspection result
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments or notes
    # -------------------------------- Parent Tables -------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="v_seh")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="v_seh")
    seh_id: Mapped[int] = mapped_column(ForeignKey("SEHTable.id"), nullable=False)
    seh = relationship("SEHTable", back_populates="v_seh")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="v_seh")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="v_seh")
    @classmethod
    def add_v_seh_entry(cls, v_seh_data: dict):
        """
        Adds a new VSEH entry to the database.

        Parameters:
        v_seh_data (dict): A dictionary containing the fields required for a VSEHTable entry.

        Returns:
        VSEHTable instance of the added entry.
        """
        try:
            # Ensure the required fields are present in v_seh_data
            required_fields = {"datetime_id", "user_id", "seh_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - v_seh_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            v_seh_entry = cls(**v_seh_data)
            db.session.add(v_seh_entry)
            db.session.commit()
            return v_seh_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class VMainBridgeTable(db.Model):
    __tablename__ = "VMainBridgeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields -----------
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image of the visual inspection result
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments or notes
    # ---------------------- parent Tables ----------------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="v_main_bridge")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="v_main_bridge")
    main_bridge_id: Mapped[int] = mapped_column(ForeignKey("MainBridgeTable.id"), nullable=False)
    main_bridge = relationship("MainBridgeTable", back_populates="v_main_bridge")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="v_main_bridge")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="v_main_bridge")
    @classmethod
    def add_v_main_bridge_entry(cls, v_main_bridge_data: dict):
        """
        Adds a new VMainBridgeTable entry to the database.

        Parameters:
        v_main_bridge_data (dict): A dictionary containing the fields required for a VMainBridgeTable entry.

        Returns:
        VMainBridgeTable instance of the added entry.
        """
        try:
            # Ensure the required fields are present in v_main_bridge_data
            required_fields = {"datetime_id", "user_id", "main_bridge_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - v_main_bridge_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            v_main_bridge_entry = cls(**v_main_bridge_data)
            db.session.add(v_main_bridge_entry)
            db.session.commit()
            return v_main_bridge_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class VStumpBridgeTable(db.Model):
    __tablename__ = "VStumpBridgeTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image of the visual inspection result
    comment: Mapped[str] = mapped_column(String(4000), nullable=True)  # Any additional comments or notes
    # ---------------------------- Parent Tables --------------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="v_stump_bridge")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="v_stump_bridge")
    stumpbridge_id: Mapped[int] = mapped_column(ForeignKey("StumpBridgeTable.id"), nullable=False)
    stump_bridge = relationship("StumpBridgeTable", back_populates="v_stump_bridge")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="v_stump_bridge")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="v_stump_bridge")
    @classmethod
    def add_v_stump_bridge_entry(cls, v_stump_bridge_data: dict):
        """
        Adds a new entry to the VStumpBridgeTable.

        Parameters:
        v_stump_bridge_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        VStumpBridgeTable instance of the added entry.
        """
        try:
            # Ensure all required fields are present
            required_fields = {"datetime_id", "user_id", "stumpbridge_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - v_stump_bridge_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            v_stump_bridge_entry = cls(**v_stump_bridge_data)
            db.session.add(v_stump_bridge_entry)
            db.session.commit()
            return v_stump_bridge_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

#------------------------- Kapton Gluing Tables ----------------------------
class KaptonGluingTable(db.Model):
    __tablename__ = "KaptonGluingTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    cooling_point: Mapped[str] = mapped_column(Enum('5cp', '6cp', name='cooling_point_enum'), nullable=False)
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image path or URL
    comment: Mapped[str] = mapped_column(Text, nullable=True)  # Comment field


    # ---------------------------- Parent Tables ---------------------------
    date_time_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="kapton_gluing")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="kapton_gluing")

    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="kapton_gluing")

    sensor_id: Mapped[int] = mapped_column(ForeignKey("SensorTable.id"), nullable=False)
    sensor = relationship("SensorTable", back_populates="kapton_gluing")

    glue_id: Mapped[int] = mapped_column(ForeignKey("GlueTable.id"), nullable=False)
    glue = relationship("GlueTable", back_populates="kapton_gluing")

    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="kapton_gluing")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="kapton_gluing")
    @classmethod
    def add_kapton_gluing_entry(cls, kapton_gluing_data: dict):
        """
        Adds a new entry to the KaptonGluingTable.

        Parameters:
        kapton_gluing_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        KaptonGluingTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"cooling_point", "date_time_id", "user_id", "temp_humi_dew_id", 
                                "sensor_id", "glue_id", "jig_id", "station_id"}
            missing_fields = required_fields - kapton_gluing_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Check if `cooling_point` has a valid enum value
            valid_cooling_points = {'5cp', '6cp'}
            if kapton_gluing_data.get("cooling_point") not in valid_cooling_points:
                raise ValueError(f"Invalid cooling point value. Allowed values: {', '.join(valid_cooling_points)}")

            # Create and commit the entry
            kapton_gluing_entry = cls(**kapton_gluing_data)
            db.session.add(kapton_gluing_entry)
            db.session.commit()
            return kapton_gluing_entry
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")


# ---------------------------  HV & IV Table -------------------------------
# Foreign key : temp_dew , datetime , sensor ,  station id
class HVTable(db.Model):
    __tablename__ = "HVTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    #fields
    cooling_point: Mapped[str] = mapped_column(Enum('5cp', '6cp', name='cooling_point_enum'), nullable=False)
    hv_csv: Mapped[str] = mapped_column(String(1000), nullable=True)  # Path or URL to HV plot CSV
    optional_file: Mapped[str] = mapped_column(String(1000), nullable=True)  # Path or URL to optional file
    comment: Mapped[str] = mapped_column(Text, nullable=True)  # Comment field
 
    # ----------------------------- Parent Tables ------------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="hv")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="hv")

    sensor_id: Mapped[int] = mapped_column(ForeignKey("SensorTable.id"), nullable=False)
    sensor = relationship("SensorTable", back_populates="hv")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="hv")

    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="hv")
    @classmethod
    def add_hv_entry(cls, hv_data: dict):
        """
        Adds a new entry to the HVTable.

        Parameters:
        hv_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        HVTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"cooling_point", "datetime_id", "user_id", 
                                "sensor_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - hv_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate cooling point
            valid_cooling_points = {'5cp', '6cp'}
            if hv_data.get("cooling_point") not in valid_cooling_points:
                raise ValueError(f"Invalid cooling point value. Allowed values: {', '.join(valid_cooling_points)}")

            # Create and commit the entry
            hv_entry = cls(**hv_data)
            db.session.add(hv_entry)
            db.session.commit()
            return hv_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class IVTable(db.Model):
    __tablename__ = "IVTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    cooling_point: Mapped[str] = mapped_column(Enum('5cp', '6cp', name='cooling_point_enum'), nullable=False)
    iv_csv: Mapped[str] = mapped_column(String(1000), nullable=True)  # Path or URL to HV plot CSV
    optional_file: Mapped[str] = mapped_column(String(1000), nullable=True)  # Path or URL to optional file
    comment: Mapped[str] = mapped_column(Text, nullable=True)  # Comment field
    # ----------------------------------- Parent Tables ---------------------------
    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="iv")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="iv")

    sensor_id: Mapped[int] = mapped_column(ForeignKey("SensorTable.id"), nullable=False)
    sensor = relationship("SensorTable", back_populates="iv")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="iv")
    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="iv")
    @classmethod
    def add_iv_entry(cls, iv_data: dict):
        """
        Adds a new entry to the IVTable.

        Parameters:
        iv_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        IVTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"cooling_point", "datetime_id", "user_id",
                                "sensor_id", "station_id", "temp_humi_dewid"}
            missing_fields = required_fields - iv_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate cooling point
            valid_cooling_points = {'5cp', '6cp'}
            if iv_data.get("cooling_point") not in valid_cooling_points:
                raise ValueError(f"Invalid cooling point value. Allowed values: {', '.join(valid_cooling_points)}")

            # Create and commit the entry
            iv_entry = cls(**iv_data)
            db.session.add(iv_entry)
            db.session.commit()
            return iv_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")


# -----------------------Sensor Gluing Table -------------------------------
#foreign key , Temp , datetime , station id , jig , 
class SensorGluingTable(db.Model):
    __tablename__ = "SensorGluingTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    bare_module_id: Mapped[int] = mapped_column(Integer, nullable=False)
    module_spacing: Mapped[float] = mapped_column(Integer, nullable=False)
    cooling_point: Mapped[str] = mapped_column(Enum('5cp', '6cp', name='cooling_point_enum'), nullable=False)
    image: Mapped[str] = mapped_column(String(1000), nullable=True)  # Image path or URL
    comment: Mapped[str] = mapped_column(Text, nullable=True)  # Comment field

    # ------------------------- Parent Tables ------------------------------
    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="sensor_gluing")

    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="sensor_gluing")

    temp_humi_dewid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="sensor_gluing")

    sensor_id: Mapped[int] = mapped_column(ForeignKey("SensorTable.id"), nullable=False)
    sensor = relationship("SensorTable", back_populates="sensor_gluing")

    mainbridgeid: Mapped[int] = mapped_column(ForeignKey("MainBridgeTable.id"), nullable=False)
    main_bridge = relationship("MainBridgeTable", back_populates="sensor_gluing")

    stumpbridge_id: Mapped[int] = mapped_column(ForeignKey("StumpBridgeTable.id"), nullable=False)
    stump_bridge = relationship("StumpBridgeTable", back_populates="sensor_gluing")

    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="sensor_gluing")

    glue_id: Mapped[int] = mapped_column(ForeignKey("GlueTable.id"), nullable=False)
    glue = relationship("GlueTable", back_populates="sensor_gluing")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="sensor_gluing")
    # ------------------------------ child Tables -----------------------------
    needle_metrology = relationship("NeedleMetrologyTable", back_populates="sensor_gluing")
    hybrid_gluing = relationship("HybridGluingTable", back_populates="sensor_gluing")
    @classmethod
    def add_sensor_gluing_entry(cls, sensor_gluing_data: dict):
        """
        Adds a new entry to the SensorGluingTable.

        Parameters:
        sensor_gluing_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        SensorGluingTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"bare_module_id", "module_spacing", "cooling_point", "datetimeid", 
                                "user_id", "temp_humi_dewid", "sensor_id", "mainbridgeid", 
                                "stumpbridge_id", "jig_id", "glue_id", "station_id"}
            missing_fields = required_fields - sensor_gluing_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate cooling point
            valid_cooling_points = {'5cp', '6cp'}
            if sensor_gluing_data.get("cooling_point") not in valid_cooling_points:
                raise ValueError(f"Invalid cooling point value. Allowed values: {', '.join(valid_cooling_points)}")

            # Create and commit the entry
            sensor_gluing_entry = cls(**sensor_gluing_data)
            db.session.add(sensor_gluing_entry)
            db.session.commit()
            return sensor_gluing_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class NeedleMetrologyTable(db.Model):
    __tablename__ = "NeedleMetrologyTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delta_x: Mapped[float] = mapped_column(Float, nullable=False)
    delta_y: Mapped[float] = mapped_column(Float, nullable=False)
    rotation: Mapped[float] = mapped_column(Float, nullable=False)
    data_file: Mapped[str] = mapped_column(String, nullable=True)  
    image: Mapped[str] = mapped_column(String, nullable=True)      # For storing image files
    comment: Mapped[str] = mapped_column(String, nullable=True)  # For storing comments
    # --------------------------- Parent tables -----------------------------------
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="needle_metrology")

    datetime_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="needle_metrology")

    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="needle_metrology")

    sensor_gluing_id: Mapped[int] = mapped_column(ForeignKey("SensorGluingTable.id"), nullable=False)
    sensor_gluing = relationship("SensorGluingTable", back_populates="needle_metrology")

    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="needle_metrology")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="needle_metrology")
    @classmethod
    def add_needle_metrology_entry(cls, needle_metrology_data: dict):
        """
        Adds a new entry to the NeedleMetrologyTable.

        Parameters:
        needle_metrology_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        NeedleMetrologyTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"user_id", "delta_x", "delta_y", "rotation", "datetime_id", 
                                "temp_humi_dew_id", "sensor_gluing_id", "jig_id", "station_id"}
            missing_fields = required_fields - needle_metrology_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            needle_metrology_entry = cls(**needle_metrology_data)
            db.session.add(needle_metrology_entry)
            db.session.commit()
            return needle_metrology_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class SkeletonTestTable(db.Model):
    __tablename__ = "SkeletonTestTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields
    skeleton_id: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_img: Mapped[str] = mapped_column(String, nullable=True)  
    comment: Mapped[str] = mapped_column(String, nullable=True) 
    # --------------------------------- parent tables ---------------------------
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="skeleton_test")

    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="skeleton_test")

    temp_humi_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="skeleton_test")

    vtrxid: Mapped[int] = mapped_column(ForeignKey("VTRxTable.id"), nullable=False)
    vtrx = relationship("VTRxTable", back_populates="skeleton_test")

    jigid: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="skeleton_test")

    groundebalancer_id: Mapped[int] = mapped_column(ForeignKey("GroundBalancerTable.id"), nullable=False)
    ground_balancer = relationship("GroundBalancerTable", back_populates="skeleton_test")

    feh_id: Mapped[int] = mapped_column(ForeignKey("FEHTable.id"), nullable=False)
    feh= relationship("FEHTable", back_populates="skeleton_test")

    seh_id: Mapped[int] = mapped_column(ForeignKey("SEHTable.id"), nullable=False)
    seh = relationship("SEHTable", back_populates="skeleton_test")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="skeleton_test")
    # -------------------- child table ------------------------------
    hybrid_gluing = relationship("HybridGluingTable", back_populates="skeleton_test")
    @classmethod
    def add_skeleton_test_entry(cls, skeleton_test_data: dict):
        """
        Adds a new entry to the SkeletonTestTable.

        Parameters:
        skeleton_test_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        SkeletonTestTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"skeleton_id", "userid", "datetimeid", "temp_humi_id", "vtrxid", 
                                "jigid", "groundebalancer_id", "feh_id", "seh_id", "station_id"}
            missing_fields = required_fields - skeleton_test_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            skeleton_test_entry = cls(**skeleton_test_data)
            db.session.add(skeleton_test_entry)
            db.session.commit()
            return skeleton_test_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class HybridGluingTable(db.Model):
    __tablename__ = "HybridGluingTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields
    upload_img: Mapped[str] = mapped_column(String, nullable=True)  # Optional image upload
    comment: Mapped[str] = mapped_column(String, nullable=True) 
    # ------------------------------- parent tables----------------------
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="hybrid_gluing")

    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="hybrid_gluing")

    tempid: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="hybrid_gluing")

    glue_id: Mapped[int] = mapped_column(ForeignKey("GlueTable.id"), nullable=False)
    glue = relationship("GlueTable", back_populates="hybrid_gluing")

    sensorgluing_id: Mapped[int] = mapped_column(ForeignKey("SensorGluingTable.id"), nullable=False)
    sensor_gluing = relationship("SensorGluingTable", back_populates="hybrid_gluing")

    skeletontest_id: Mapped[int] = mapped_column(ForeignKey("SkeletonTestTable.id"), nullable=False)
    skeleton_test = relationship("SkeletonTestTable", back_populates="hybrid_gluing")

    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="hybrid_gluing")

    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="hybrid_gluing")
    # ------------------------- child tables ---------------------------------
    module_encapsulation = relationship("ModuleEncapsulationTable", back_populates="hybrid_gluing")
    wire_bonding = relationship("WireBondingTable", back_populates="hybrid_gluing")
    noise_test1 = relationship("NoiseTest1Table", back_populates="hybrid_gluing")
    noise_test2 = relationship("NoiseTest2Table", back_populates="hybrid_gluing")
    burnin_test = relationship("BurninTestTable", back_populates="hybrid_gluing")
    @classmethod
    def add_hybrid_gluing_entry(cls, hybrid_gluing_data: dict):
        """
        Adds a new entry to the HybridGluingTable.

        Parameters:
        hybrid_gluing_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        HybridGluingTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"userid", "datetimeid", "tempid", "glue_id", "sensorgluing_id", 
                            "skeletontest_id", "jig_id", "station_id"}
            missing_fields = required_fields - hybrid_gluing_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            hybrid_gluing_entry = cls(**hybrid_gluing_data)
            db.session.add(hybrid_gluing_entry)
            db.session.commit()
            return hybrid_gluing_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class ModuleEncapsulationTable(db.Model):
    __tablename__ = "ModuleEncapsulationTable"
    primary: Mapped[int] = mapped_column(Integer, primary_key=True )
    #fields 
    preparation_time: Mapped[float] = mapped_column(Float, nullable=False)  # Time for glue preparation
    comment: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment
    image: Mapped[str] = mapped_column(String, nullable=True)  # Optional image (path or URL)

    #foreigntables ---------------------- parent tables ----------------------------
    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="module_encapsulation")
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user  = relationship("UserTable", back_populates="module_encapsulation")
    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="module_encapsulation")
    hybridgluing_id: Mapped[int] = mapped_column(ForeignKey("HybridGluingTable.id"), nullable=False)
    hybrid_gluing = relationship("HybridGluingTable", back_populates="module_encapsulation")
    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="module_encapsulation")
    glue_id: Mapped[int] = mapped_column(ForeignKey("GlueTable.id"), nullable=False)
    glue = relationship("GlueTable", back_populates="module_encapsulation")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="module_encapsulation")
    @classmethod
    def add_module_encapsulation_entry(cls, module_encapsulation_data: dict):
        """
        Adds a new entry to the ModuleEncapsulationTable.

        Parameters:
        module_encapsulation_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        ModuleEncapsulationTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"preparation_time", "datetimeid", "userid", "temp_humi_dew_id", 
                            "hybridgluing_id", "jig_id", "glue_id", "station_id"}
            missing_fields = required_fields - module_encapsulation_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            module_encapsulation_entry = cls(**module_encapsulation_data)
            db.session.add(module_encapsulation_entry)
            db.session.commit()
            return module_encapsulation_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class WireBondingTable(db.Model):
    __tablename__ = "WireBondingTable"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields
    comment: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment
    upload_img: Mapped[str] = mapped_column(String, nullable=True)  # Optional image upload
    excel_file: Mapped[str] = mapped_column(String, nullable=True)  # Optional Excel or CSV data file
    
    # Delta heights
    delta_height_top: Mapped[float] = mapped_column(Float, nullable=True)  # Delta height for top
    delta_height_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # Delta height for bottom
    
    # Correction factors K1 (SEN)
    correction_factor_K1_top: Mapped[float] = mapped_column(Float, nullable=True)  # K1 for top
    correction_factor_K1_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # K1 for bottom
    
    # Correction factors K2 (FEH)
    correction_factor_K2_top: Mapped[float] = mapped_column(Float, nullable=True)  # K2 for top
    correction_factor_K2_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # K2 for bottom
    
    # Mean Force values
    mean_force_1_top: Mapped[float] = mapped_column(Float, nullable=True)  # Mean Force 1 for top
    mean_force_1_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # Mean Force 1 for bottom
    mean_force_2_top: Mapped[float] = mapped_column(Float, nullable=True)  # Mean Force 2 for top
    mean_force_2_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # Mean Force 2 for bottom
    
    # Rms values
    rms_value_top: Mapped[float] = mapped_column(Float, nullable=True)  # RMS Value for top
    rms_value_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # RMS Value for bottom
    
    # Standard Deviation values
    std_deviation_top: Mapped[float] = mapped_column(Float, nullable=True)  # Standard Deviation for top
    std_deviation_bottom: Mapped[float] = mapped_column(Float, nullable=True)  # Standard Deviation for bottom
    #Relation with other tables
    # ------------------ parent table --------------------------------
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user  = relationship("UserTable", back_populates="wire_bonding")
    date_time_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="wire_bonding")
    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="wire_bonding")
    hybrid_gluing_id: Mapped[int] = mapped_column(ForeignKey("HybridGluingTable.id"), nullable=False)
    hybrid_gluing = relationship("HybridGluingTable", back_populates="wire_bonding")
    jig_id: Mapped[int] = mapped_column(ForeignKey("JigTable.id"), nullable=False)
    jig = relationship("JigTable", back_populates="wire_bonding")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="wire_bonding")
    @classmethod
    def add_wire_bonding_entry(cls, wire_bonding_data: dict):
        """
        Adds a new entry to the WireBondingTable.

        Parameters:
        wire_bonding_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        WireBondingTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"userid", "date_time_id", "temp_humi_dew_id", 
                            "hybrid_gluing_id", "jig_id", "station_id"}
            missing_fields = required_fields - wire_bonding_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            wire_bonding_entry = cls(**wire_bonding_data)
            db.session.add(wire_bonding_entry)
            db.session.commit()
            return wire_bonding_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class NoiseTest1Table(db.Model):
    __tablename__ = "NoiseTest1Table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    file_1: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 1
    file_2: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 2
    file_3: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 3
    file_4: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 4
    file_5: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 5
    comment: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment
    # Relationship with othertables 
    # --------------- parents--------------------------------
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="noise_test1")
    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="noise_test1")
    temp_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="noise_test1")
    hybrid_gluing_id: Mapped[int] = mapped_column(ForeignKey("HybridGluingTable.id"), nullable=False)
    hybrid_gluing = relationship("HybridGluingTable", back_populates="noise_test1")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="noise_test1")
    @classmethod
    def add_noise_test1_entry(cls, noise_test1_data: dict):
        """
        Adds a new entry to the NoiseTest1Table.

        Parameters:
        noise_test1_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        NoiseTest1Table instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"user_id", "datetimeid", "temp_id", "hybrid_gluing_id", "station_id"}
            missing_fields = required_fields - noise_test1_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            noise_test1_entry = cls(**noise_test1_data)
            db.session.add(noise_test1_entry)
            db.session.commit()
            return noise_test1_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class NoiseTest2Table(db.Model):
    __tablename__ = "NoiseTest2Table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True )
    # fields 
    file_1: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 1
    file_2: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 2
    file_3: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 3
    file_4: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 4
    file_5: Mapped[str] = mapped_column(String, nullable=True)  # Optional file upload 5
    comment: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment
    # Relationship with othertables
    # ------------------- parents ------------------------------------
    user_id: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="noise_test2")
    datetimeid: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="noise_test2")
    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="noise_test2")
    hybrid_gluing_id: Mapped[int] = mapped_column(ForeignKey("HybridGluingTable.id"), nullable=False)
    hybrid_gluing = relationship("HybridGluingTable", back_populates="noise_test2")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="noise_test2")
    @classmethod
    def add_noise_test2_entry(cls, noise_test2_data: dict):
        """
        Adds a new entry to the NoiseTest2Table.

        Parameters:
        noise_test2_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        NoiseTest2Table instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"user_id", "datetimeid", "temp_humi_dew_id", "hybrid_gluing_id", "station_id"}
            missing_fields = required_fields - noise_test2_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            noise_test2_entry = cls(**noise_test2_data)
            db.session.add(noise_test2_entry)
            db.session.commit()
            return noise_test2_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

class BurninTestTable(db.Model):
    __tablename__ = "BurninTestTable"
    primary_id: Mapped[int] = mapped_column(Integer, primary_key=True )
    #fields
    tracker_monitor_root_file: Mapped[str] = mapped_column(String, nullable=True)  # Tracker Monitor Root file
    comment: Mapped[str] = mapped_column(String, nullable=True)  # Optional comment
    tracker_root_file: Mapped[str] = mapped_column(String, nullable=True)  # Tracker Root File
    press_supply_root_file: Mapped[str] = mapped_column(String, nullable=True)  # Press Supply Root File
    burnin_box_root_file: Mapped[str] = mapped_column(String, nullable=True)  # Burnin Box Root File

    # ------------------------ parent tables -------------------------------
    userid: Mapped[int] = mapped_column(ForeignKey("UserTable.id"), nullable=False)
    user = relationship("UserTable", back_populates="burnin_test")
    date_time_id: Mapped[int] = mapped_column(ForeignKey("DateTimeTable.id"), nullable=False)
    date_time = relationship("DateTimeTable", back_populates="burnin_test")
    temp_humi_dew_id: Mapped[int] = mapped_column(ForeignKey("TempHumiDewTable.id"), nullable=False)
    temp_humi_dew = relationship("TempHumiDewTable", back_populates="burnin_test")
    hybri_gluing_id: Mapped[int] = mapped_column(ForeignKey("HybridGluingTable.id"), nullable=False)
    hybrid_gluing = relationship("HybridGluingTable", back_populates="burnin_test")
    station_id: Mapped[int] = mapped_column(ForeignKey("StationTable.id"), nullable=False)
    station =relationship("StationTable",back_populates="burnin_test")
    @classmethod
    def add_burnin_test_entry(cls, burnin_test_data: dict):
        """
        Adds a new entry to the BurninTestTable.

        Parameters:
        burnin_test_data (dict): A dictionary containing the fields for the new entry.

        Returns:
        BurninTestTable instance of the added entry.
        """
        try:
            # Validate required fields
            required_fields = {"userid", "date_time_id", "temp_humi_dew_id", "hybri_gluing_id", "station_id"}
            missing_fields = required_fields - burnin_test_data.keys()

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Create and commit the entry
            burnin_test_entry = cls(**burnin_test_data)
            db.session.add(burnin_test_entry)
            db.session.commit()
            return burnin_test_entry

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")

# ------------------ remove ---------------------------------------





