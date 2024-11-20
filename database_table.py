from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Boolean, DateTime , Text
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
import os

import datetime
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

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


class MaterialReceiverTable(db.Model):
    __tablename__ = 'material_receivers_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensors_quantity = mapped_column(Integer)
    hybrid_quantity = mapped_column(Integer)
    optical_fibres_quantity = mapped_column(Integer)
    kaptontapes_quantity = mapped_column(Integer)
    bridges_quantity = mapped_column(Integer)
    # add others in the comment box
    
    receiver_name: Mapped[str] = mapped_column(String(100), nullable=False)
    others:Mapped[bool] = mapped_column(Boolean, default=False)  
    date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    image_url: Mapped[str] = mapped_column(String(200),nullable =True)  # Store the filename or file path
    comment: Mapped[str] = mapped_column(Text)

# VisualInspection Table
class VisualInspectionSensorTable(db.Model):
    __tablename__ = 'visual_inspections_sensor_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    sensor_id: Mapped[str] = mapped_column(String(200), nullable=False)
    sensor_image: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

class VisualInspectionHybridTable(db.Model):
    __tablename__ = 'visual_inspections_hybrid_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    hybrid_id: Mapped[str] = mapped_column(String(200), nullable=False)
    hybrid_image: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)
class VisualInspectionBridgeTable(db.Model):
    __tablename__ = 'visual_inspections_bridge_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    bridge_id: Mapped[str] = mapped_column(String(200), nullable=False)
    bridge_image: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)
# KaptonGluing Table (5cp)
class KaptonGluingTable(db.Model):
    __tablename__ = 'kapton_gluings_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    sensor_id: Mapped[str] = mapped_column(String(1000), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    cooling_points: Mapped[str] = mapped_column(String(50), nullable=False)
    main_bridge_type: Mapped[str] = mapped_column(String(100))
    main_bridge_id =  mapped_column(String(1000), nullable=False)
    stump_bridge_type: Mapped[str] = mapped_column(String(100))
    stump_bridge_id =  mapped_column(String(1000), nullable=False)
    part_A_batch_no: Mapped[str] = mapped_column(String(100))
    part_A_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    part_B_batch_no: Mapped[str] = mapped_column(String(100))
    part_B_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    image_url:Mapped[str] = mapped_column(String(200),nullable =True)
    comment: Mapped[str] = mapped_column(Text)


# HvIvForm Table
class HvIvFormTable(db.Model):
    __tablename__ = 'hv_iv_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    sensor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    cooling_points: Mapped[str] = mapped_column(String(50), nullable=False)
    hv_plot_url: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    iv_plot_url: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    csv_url: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    image_url:Mapped[str] = mapped_column(String(200),nullable =True)
    comment: Mapped[str] = mapped_column(Text)

# SensorGluing Table
class SensorGluingTable(db.Model):
    __tablename__ = 'sensor_gluings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    bare_module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    top_sensor: Mapped[str] = mapped_column(String(100), nullable=False)
    bottom_sensor: Mapped[str] = mapped_column(String(100), nullable=False)
    main_bridge: Mapped[str] = mapped_column(String(100), nullable=False)
    stump_bridge: Mapped[str] = mapped_column(String(100), nullable=False)
    module_spacing: Mapped[str] = mapped_column(String(50), nullable=False)
    cooling_points: Mapped[str] = mapped_column(String(50), nullable=False)
    jigs: Mapped[str] = mapped_column(String(50), nullable=False)
    part_A_batch_no: Mapped[str] = mapped_column(String(100))
    part_A_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    part_B_batch_no: Mapped[str] = mapped_column(String(100))
    part_B_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    image_url: Mapped[str] = mapped_column(String(200),nullable =True)  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# NeedleMetrologyForm Table
class NeedleMetrologyTable(db.Model):
    __tablename__ = 'needle_metrology'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    bare_module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    x_coordinate: Mapped[str] = mapped_column(String(50), nullable=False)
    y_coordinate: Mapped[str] = mapped_column(String(50), nullable=False)
    del_theta: Mapped[str] = mapped_column(String(50), nullable=False)
    csv_xl_url: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    image_url: Mapped[str] = mapped_column(String(200),nullable =True)  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# SkeletonTestForm Table
class SkeletonTestTable(db.Model):
    __tablename__ = 'skeleton_test'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    skeleton_id: Mapped[str] = mapped_column(String(100), nullable=False)
    FEH_L: Mapped[str] = mapped_column(String(100), nullable=False)
    FEH_R: Mapped[str] = mapped_column(String(100), nullable=False)
    VTRx: Mapped[str] = mapped_column(String(100), nullable=False)
    ground_balancer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    root_file_url: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# HybridGluingForm Table
class HybridGluingTable(db.Model):
    __tablename__ = 'hybrid_gluing_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    bare_module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    skeleton_id: Mapped[str] = mapped_column(String(100), nullable=False)
    part_A_batch_no: Mapped[str] = mapped_column(String(100))
    part_A_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    part_B_batch_no: Mapped[str] = mapped_column(String(100))
    part_B_exp_date: Mapped[datetime.date] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    image_url: Mapped[str] = mapped_column(String(200), nullable= True)  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# ModuleData Table
class ModuleDataTable(db.Model):
    __tablename__ = 'module_data_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    comment: Mapped[str] = mapped_column(Text)

# WireBondingForm Table
class WireBondingTable(db.Model):
    __tablename__ = 'wire_bonding_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    module_id: Mapped[str] = mapped_column(String(100), nullable=False)
    pull_test_result: Mapped[str] = mapped_column(Integer, nullable=False)  # Takes number
    image: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# NoiseTestForm Table
class NoiseTestTable(db.Model):
    __tablename__ = 'noise_test_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    check_id: Mapped[str] = mapped_column(String(100), nullable=False)
    root_file: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    image: Mapped[str] = mapped_column(String(200))  # Store filename or file path
    comment: Mapped[str] = mapped_column(Text)

# BurNimForm Table
class BurNimTable(db.Model):
    __tablename__ = 'burnim_test_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    module_quantity = mapped_column(Integer)
    burnim_box_result: Mapped[str]= mapped_column(String(1000), nullable=False)
    module1_id: Mapped[str] = mapped_column(String(100), nullable=False)
    module1_test_file: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    module2_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module2_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module3_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module3_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module4_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module4_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module5_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module5_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module6_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module6_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module7_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module7_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module8_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module8_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module9_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module9_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    
    module10_id: Mapped[str] = mapped_column(String(100), nullable=True)
    module10_test_file: Mapped[str] = mapped_column(String(1000), nullable=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable= True)
    comment: Mapped[str] = mapped_column(Text,nullable= True)



