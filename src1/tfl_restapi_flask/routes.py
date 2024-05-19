from flask import current_app as app
from flask import jsonify, request
from tfl_restapi_flask.models import User, CyclingAndWeather,SavedCharts, user_schema, CyclingAndWeather_schema, SavedCharts_schema
from tfl_restapi_flask import db
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

#0. API Default Return Message
@app.route('/',methods=['GET'])
def hello():
    return ("London Cycling and Weather API")

#1. GET Methods for getting all data at once
@app.route('/user',methods=['GET'])
def get_all_users():
    users = User.get_all()
    user_serialiser = user_schema(many=True)
    data = user_serialiser.dump(users)
    return jsonify(data),200

@app.route('/cyclingandweather',methods=['GET'])
def get_all_data():
    cyclingdata = CyclingAndWeather.get_all()
    cyclingdata_serialiser = CyclingAndWeather_schema(many=True)
    data = cyclingdata_serialiser.dump(cyclingdata)
    return jsonify(data),200

#2. GET methods for getting a specific row of data
@app.route('/user/<int:id>',methods=['GET'])
def get_user_by_id(id):
    try:
        found_user = User.get_by_id(id)
        user_serialiser = user_schema(many=False)
        data = user_serialiser.dump(found_user)
        app.logger.info(f"Successfull client reqeust for user data with id: {id}")
        return jsonify(data),200
    except:
        app.logger.error(f'UNsuccessfull client request. User with id: {id} not found')
        return jsonify({'message': f"No user found with this id"}), 404

@app.route('/cyclingandweather/<int:id>',methods=['GET'])
def get_cycling_by_id(id):
    try:
        found_data = CyclingAndWeather.get_by_id(id)
        data_serialiser = CyclingAndWeather_schema(many=False)
        data = data_serialiser.dump(found_data)
        app.logger.info(f"Successfull client reqeust for cycling and weather data with id: {id}")
        return jsonify(data),200
    except:
        app.logger.error(f'UNsuccessfull client request. Cycling and weather data with id: {id} not found')
        return jsonify({'message': f"No data found with this id"}), 404

"""
Note:Post, put, and delete methods are only used for the user database, since the weather database is complete and
not intended to be edited by clients of the API
"""
#3. POST methods
@app.route('/user/new',methods=['POST'])
def create_user():
    user_json = request.get_json()
    try:
        #create new user object. Id primary key atribute is automatically set and thus set to None
        new_user = User(None,user_json.get('email'),user_json.get('password'))
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"New user with email: {new_user.email} successfully created")
        return jsonify({'message': f"User created. Email: {new_user.email}. ID: {new_user.id}"}), 201
    except:
        app.logger.error(f'Passed email already in use')
        return jsonify({'message': f"Email already in use. Login or choose different email"}), 409

@app.route('/user/login',methods=['POST'])
def verify_login():
    login_json = request.get_json()
    #attempt to find user by email
    try:
        attempt_user = User.get_by_email(login_json.get('email'))
    except:
        app.logger.error(f'No user found with passed email')
        return jsonify({'message': f"No user found with this email"}), 404
    if attempt_user.verify_pw(login_json.get('password')):
        app.logger.info(f"Successfull login of: email: {attempt_user.getEmail()}")
        user_charts = SavedCharts.get_by_id(attempt_user.getId())
        charts_serialiser = SavedCharts_schema(many=True)
        chartsData = charts_serialiser.dump(user_charts)
        return jsonify(attempt_user.getId(),chartsData),200
    else:
        app.logger.info(f"Unsuccessfull login attempt for email: {attempt_user.getEmail()}")
        return jsonify({'message': f"Login Failed"}), 401


@app.route('/createchart',methods=['POST'])
def create_chart():
    chart_json = request.get_json()
    #create new user object. Id primary key atribute is automatically set and thus set to None
    new_chart = SavedCharts(chart_json.get('name'),chart_json.get('user_id'),chart_json.get('start_date'),chart_json.get('end_date'),chart_json.get('data_type'),chart_json.get('plot_type'))
    db.session.add(new_chart)
    db.session.commit()
    app.logger.info(f"chart successfully created")
    return jsonify({'chart_id': new_chart.get_fig_id()}), 201






#4. PUT methods:
@app.route('/user/edit',methods=['PUT'])
def update_user_info():
    change_request_json = request.get_json()
    #attempt to find user by email
    try:
        existing_user = User.get_by_email(change_request_json.get('old_email'))
        id = existing_user.id
    except:
        app.logger.error(f'No user found with passed email')
        return jsonify({'message': f"No user found with this email"}), 404
    #verify email and password before allowing user to edit details
    if existing_user.verify_pw(change_request_json.get('old_password')):
        #delete old record in order to add in new updated record
        db.session.delete(existing_user)
        edited_user = User(id,change_request_json.get('new_email'),change_request_json.get('new_password'))
        db.session.add(edited_user)
        # Commit the changes to the database
        db.session.commit()
        app.logger.info(f'User with id: {edited_user.id} successfully changed email/password. Email: {edited_user.email}')
        return jsonify({'message': f"User details updated. Email: {edited_user.email}. ID: {edited_user.id}"}), 201
    else:
        app.logger.info(f'UNsuccessfull attempt to change details for user with with id: {existing_user.id} ')
        return jsonify({'message': "Login failed, user details NOT changed"}), 401

#5. DELETE methods:
@app.route('/user/delete',methods=['DELETE'])
def delete_user():
    delete_request_json = request.get_json()
    #attempt to find user by email
    try:
        existing_user = User.get_by_email(delete_request_json.get('email'))
    except:
        app.logger.error(f'No user found with passed email')
        return jsonify({'message': f"No user found with this email"}), 404
    #check if email and password match to allow user to be deleted
    if existing_user.verify_pw(delete_request_json.get('password')):
        #delete user and commit change to db
        db.session.delete(existing_user)
        db.session.commit()
        app.logger.info(f'User with id: {existing_user.id} successfully deleted')
        return jsonify({'message': f"User deleted. Email: {existing_user.email}. ID: {existing_user.id}"}), 200
    else:
        app.logger.info(f'UNsuccessfull attempt to delete user with id: {existing_user.id}')
        return jsonify({'message': "Login failed, user NOT deleted"}), 401