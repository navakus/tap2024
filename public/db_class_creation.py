from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
import os
import dotenv
dotenv.load_dotenv(override=True)

user_name = 'admin'
password = 'tap123123'
host_bd = '@tap.cilqagfogfw8.ap-southeast-1.rds.amazonaws.com/tap'

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + user_name + ':' + password + \
    host_bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}
db = SQLAlchemy(app)
db.metadata.clear()

        
class Account(db.Model):
    __tablename__ = "account"

    email = db.Column(db.String(320), primary_key=True)
    account_name = db.Column(db.String(45))
    password = db.Column(db.String(45))
    application = db.relationship(
        "Application", back_populates="account", cascade="all,delete-orphan")
  

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)

        return result

    def json(self):
        # dto == data transfer object
        dto = {
            "email": self.email,
            "account_name": self.account_name,
            "password": self.password,
        }

        # print("dto ", dto)
        return dto
    
class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(45))

    application = db.relationship(
        "Application", back_populates="job", cascade="all,delete-orphan")

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)

        return result

    def json(self):
        # dto == data transfer object
        dto = {
            "id": self.id,
            "jobname": self.team_name,

        }

        print("dto ", dto)
        return dto

class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), db.ForeignKey(
        "account.email"), primary_key=False)
    jobid = db.Column(db.ForeignKey(
        "job.id"), primary_key=False)
    
    account = db.relationship(
        'Account', back_populates='application')
    job = db.relationship(
        'Job', back_populates='application')

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)

        return result

    def json(self):
        # dto == data transfer object
        dto = {
            "email": self.email,
            "jobid": self.jobid,

        }

        print("dto ", dto)
        return dto
