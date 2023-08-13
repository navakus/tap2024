# Flask app for api services

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import sys
import dotenv
import string
import random
import re

dotenv.load_dotenv(override=True)

#In order to use unit test and regression test at the same time
sys.path.append("src/flask")
import db_class_creation as db_class

user_name = 'admin'
password = 'tap123123'
host_bd = '@tap.cilqagfogfw8.ap-southeast-1.rds.amazonaws.com/tap'

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + user_name + ':' + password + \
    host_bd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}
db = SQLAlchemy(app)
CORS(app)

############## Register #############
@app.route("/createaccount",methods=["POST"])
def create_account():
    if request.is_json:
        try:
            #Check all the fields are inputted
            data = request.get_json()
            if data["email"] != "":
                email = data["email"]
            if data["name"] != "":
                name = data["name"]
            if data["password"] != "":
                password = data["password"]

           
            account = db_class.Account(
                email=email, account_name=name, password=password)
            try:
                db.session.add(account)
                db.session.commit()
                return jsonify({
                    "code": 200,
                    "message": "Account created!"
                }), 200
            except Exception as e:
                # unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 401,
                    "message": "Duplicate email"
                }), 401
        except Exception as e:
            # unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 406,
                "message": "Creation fail!"
            }), 406

   
    
############## View Account for admin purpose #############
@app.route("/viewaccount/<email>")
def view_account(email):
    account = db.session.query(db_class.Account).filter_by(
        email=email).first()
    if account:
        return jsonify(
            {
                "code": 200,
                "status": {
                    "Account": account.json()
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no accounts."
        }
    ), 404


############## LOGIN #############
@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        try:
            #Check all the fields are inputted
            data = request.get_json()
            print(data)
            password = data["password"]
            email = data["email"]
            account = db.session.query(db_class.Account).filter_by(
                email=email).first()
            if account:
                # print(account.email)
                if account.password == password:
                    return jsonify(
                        {
                            "code": 200,
                            "user": {"email": account.email, "name": account.account_name}
                        }
                    ), 200
                else:
                    return jsonify(
                        {
                            "code": 403,
                            "message": "Incorrect password"
                        }
                    ), 403

            return jsonify(
                {
                    "code": 404,
                    "message": "There are no account associated with that email. Please sign up for an account!"
                }
            ), 404
        except Exception as e:
            # unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 401,
                "message": "Request error!"
            }), 401

############## Job Application #############
@app.route("/apply",methods=["POST"])
def apply():
    if request.is_json:
        try:
            #Check all the fields are inputted
            data = request.get_json()
            if data["email"] != "":
                email = data["email"]
            if data["jobid"] != "":
                jobid = data["jobid"]

            if db.session.query(db_class.Application).filter_by(
            email=email, jobid=jobid).first():
                return jsonify({
                    "code": 402,
                    "message": "Job already applied!"
                }), 402

           
            account = db_class.Application(
                email=email, jobid=jobid)
            try:
                db.session.add(account)
                db.session.commit()
                return jsonify({
                    "code": 200,
                    "message": "Successfully applied to job!"
                }), 200
            except Exception as e:
                # unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 401,
                    "message": "Error applying to job!"
                }), 401
        except Exception as e:
            # unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 406,
                "message": "No inputs for email or jobid"
            }), 406

            





############## GET Job Applications By User #############
@app.route("/getapplications/<email>", methods=["GET"])
def get_applications(email):
    apps = db.session.query(db_class.Application).filter_by(
            email=email).all()
    if apps:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "apps": [j.json() for j in apps]
                }
            }), 200
    else:
        return jsonify(
            {
            "code": 404,
            "message": "No application found!"
            }          
        ), 404

############## Withdraw Application #############
@app.route("/withdraw", methods=["DELETE"])
def withdraw_job():
     if request.is_json:
        try:
            #Check all the fields are inputted
            data = request.get_json()
            if data["email"] != "":
                email = data["email"]
            if data["jobid"] != "":
                jobid = data["jobid"]
          

            try:
                job = db.session.query(db_class.Application).filter_by(email=email, jobid=jobid).delete()  
                db.session.commit()
                return jsonify({
                        "code": 201,
                        "data": {
                            "message": "Job Application sucessfully withdrawn!"
                        }
                    }), 201
            except Exception as e:
                # unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)
                return jsonify({
                        "code": 401,
                        "message": "Unable to delete job application!"
                    }), 401
            
        except Exception as e:
                # unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)
                return jsonify({
                        "code": 404,
                        "message": "Email or jobid missing"
                    }), 404
        

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": Account")
    app.run(host='0.0.0.0', port=5004, debug=True)
