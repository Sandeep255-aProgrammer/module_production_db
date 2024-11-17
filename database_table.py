from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Boolean, DateTime
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


