# Adapted from https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#define-models

from typing import List
from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tfl_restapi_flask import db
from marshmallow import Schema,fields
import bcrypt

#Data base model for cycling and weather data below
class CyclingAndWeather(db.Model):
    __tablename__ = "cyclingandweather"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    date: Mapped[str] = mapped_column(db.String, nullable=False)
    temp: Mapped[float] = mapped_column(db.Float, nullable=False)
    precip: Mapped[float] = mapped_column(db.Float, nullable=False)
    NumBicylces: Mapped[int] = mapped_column(db.Integer, nullable=False)
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
class SavedCharts(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    start_date: Mapped[str] = mapped_column(db.String, nullable=False)
    end_date: Mapped[str] = mapped_column(db.String, nullable=False)
    data_type: Mapped[int] = mapped_column(db.Integer, nullable=False)
    plot_type: Mapped[int] = mapped_column(db.Integer, nullable=False)
    def __init__(self,name,user_id,start_date,end_date,data_type,plot_type):
        self.name = name
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.data_type = data_type
        self.plot_type = plot_type
    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter_by(user_id = id).all()
    def get_fig_id(self):
        return self.id

#Data base model for user information below
class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.Text, nullable=False)

    def __init__(self,id,email,password):
        self.id = id
        self.email = email
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_pw(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)
    
    def getEmail(self):
        return self.email
    def getId(self):
        return self.id
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def get_by_email(cls,email):
        return cls.query.filter_by(email=email).first_or_404()


#Data base schemas for serialisation below
class user_schema(Schema):
    id = fields.Integer()
    email =  fields.String()
    password_hash = fields.String()

class CyclingAndWeather_schema(Schema):
    id = fields.Integer()
    date = fields.String()
    temp = fields.Float()
    precip = fields.Float()
    NumBicylces = fields.Integer()

class SavedCharts_schema(Schema):
    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()
    start_date = fields.String()
    end_date = fields.String()
    data_type = fields.Integer()
    plot_type = fields.Integer()