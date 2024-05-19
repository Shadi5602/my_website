from flask import current_app as app
import os
from flask import Flask, render_template, request, jsonify, session, send_from_directory
import requests
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from tfl_frontend_flask import scatter_plot, extract_column_as_list, filter_json_data_by_date,buildChart,API_PORT
API_URL = "http://127.0.0.1:"+API_PORT

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
filename = 'plot.png'
filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)


@app.route('/')
def home():
    #Check if API is available. If API is unavailable, display warning html    
    try:
        requests.get(f"{API_URL}/")
        return render_template('home.html')
    except:
        return render_template('error.html'),404


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup/verify',methods=['POST'])
def verifysignup():
    email = request.form.get('email')
    password = request.form.get('password')
    api_sign_up_url = f"{API_URL}/user/new"
    user_data = {
        "email":email,
        "password":password
    }
    if not email or not password:
        return render_template('signup.html',details_message = 'Unable to signup, ensure all necessary fields are filled',text_color = 'red')
    try:

        response = requests.post(api_sign_up_url,json=user_data)
    except:
        return render_template("error.html")
    if response.status_code == 201:
        return render_template('signup.html',details_message = "Succesful Signup. Please move to login tab to access acount.",text_color = 'blue')
    else:
        return render_template('signup.html',details_message = 'Unable to signup, user already exists.',text_color = 'red')




@app.route('/login/verify',methods=['POST'])
def verifyLogin():
    #Secondary data clear up to ensure no data from previous user remains
    session.pop('user', None)
    session.pop('user_charts',None)

    #The code below makes a post request to the API with the user details entered. Based on the response, the code will either redirect
    #to a logged in user page or show an error message if the entered details have no match in the user database (based on the API response)
    email = request.form.get('email')
    password = request.form.get('password')
    api_login_url = f"{API_URL}/user/login"
    user_data = {
        "email":email,
        "password":password
    }
    try:
        response = requests.post(api_login_url,json=user_data)
    except:
        return render_template("error.html")
    if response.status_code == 200:
        response_data =response.json()
        user_data = {
        "email":email,
        "user_id":response_data[0]
        }
        session['user'] = user_data
        session['user_charts'] = response_data[1]
        return render_template('loggedIn.html',email = email),200
    else:
        return render_template('login.html',incorrect_details_message = 'Email and password do not match. Try again.'),403


@app.route('/loggedin')
def loggedin():
    #implement solution where routes pass logged in user detail to each other
    return render_template('loggedIn.html',email = session['user'].get('email'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_charts',None)
    return render_template('home.html')


@app.route('/createchart')
def create_chart_page():
    user_data = session['user']
    return render_template('create_chart.html',email = user_data.get('email'))


@app.route('/createchart/chartdetails',methods = ['POST'])
def create_chart():

    ##PLOT DETAILS
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    data_type = request.form.get('data_type')
    plot_type = request.form.get('plot_type')
    #END PLOT DETAILS

    #check if any form entry is NULL
    if not (name and start_date and end_date and data_type and plot_type):
        return render_template ('create_chart.html',email = session['user'].get('email'),details_message = f"Failed. Please fill/select all fields.",message_color = "red")
    else:
        try:
            datetime.datetime.strptime(start_date, '%d/%m/%Y')
            datetime.datetime.strptime(end_date, '%d/%m/%Y')
        except:
            return render_template ('create_chart.html',email = session['user'].get('email'),details_message = f"Failed. Ensure dates are entered in correct format!",message_color = "red")
    #Save user chart in API's saved charts database so user can access charts later (even after logout)
    post_saved_chart_api_url = f"{API_URL}/createchart"
    chart_data = {
        "name":name,
        "user_id":session['user'].get('user_id'),
        "start_date":start_date,
        "end_date":end_date,
        "data_type":data_type,
        "plot_type":plot_type
    }
    try:
        response = requests.post(post_saved_chart_api_url,json=chart_data)
    except:
        return render_template("error.html")
    chart_id = response.json()
    chart_data['id'] = chart_id.get('chart_id')
    #Update saved charts in session to allow user to immedietly view saved charts
    chartsList = session['user_charts']
    chartsList.append(chart_data)
    session['user_charts'] = chartsList
    return render_template ('create_chart.html',email = session['user'].get('email'),details_message = f"Chart saved! Chart id: {chart_id.get('chart_id')}",message_color = "blue")

@app.route('/viewchart',methods = ['POST'])
def ViewaChart():
    fig_id = ""
    if request.form.get('fig_id'):
        fig_id = int(request.form.get('fig_id'))

    #find user-specified chart by iterating through session's charts
    chartsList = session['user_charts']
    fig_found = 0
    for data in chartsList:
        if data.get('id') == fig_id:
            fig_data = data
            fig_found = 1

    if not fig_found:
        if session['user_charts']:
            return render_template("viewSelection.html",email = session['user'].get('email'),details_message = "Please make a selection.",charts=chartsList,img=0)
        else:
            return render_template("viewSelection.html",email = session['user'].get('email'),details_message = "Looks like you haven't created any charts. Move to the 'Create a chart' tab to create you own charts now!",charts=chartsList,img=0)
    
    #if user has made an appropriate selection, a request is sent to the API to retreive the cycling data
    get_data_api_url = f"{API_URL}/cyclingandweather"
    try:
        response = requests.get(get_data_api_url)
    except:
        return render_template("error.html")
    cycling_data = response.json()
    #build the chart using the data returned from the API (so it is loaded by html page rendered)
    buildChart(fig_data.get('name'),fig_data.get('start_date'),fig_data.get('end_date'),int(fig_data.get('data_type')),int(fig_data.get('plot_type')),filepath,cycling_data)
    return render_template('viewSelection.html',email = session['user'].get('email'),charts=chartsList,img=1)




#This route is used to access files saved in the directory file "uploads", which allows the app to dislpay created charts via 
#matplotlib.pyplot
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/viewSelection')
def viewSelectionPage():
    charts = session['user_charts']
    if session['user_charts']:
            return render_template('viewSelection.html',email = session['user'].get('email'),charts = charts,img=0)
    else:
        return render_template("viewSelection.html",email = session['user'].get('email'),details_message = "Looks like you haven't created any charts. Move to the 'Create a chart' tab to create you own charts now!",charts=charts,img=0)
    