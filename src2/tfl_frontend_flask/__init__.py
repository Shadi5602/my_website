## DEFINE API PORT ## 
API_PORT = "5001"
##  ##  ##  ##  ##  ##

import os
from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    #adapted from COMP0034 week 2 tutorial
    app = Flask(__name__, instance_relative_config=True)
    app.logger.info(f"Starting app from AppFiles")
    app.config.from_mapping(
        SECRET_KEY='RB3M2sQk7gLaMrsUtGiEVg',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'AppFiles.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)


    with app.app_context():

        from tfl_frontend_flask import routes
        
    return app


#function will return temp vs num_bikes_rented
def scatter_plot(name,x,y,axschoice,start_date,end_date,filepath):
    #function adapted from own cw1 comp0035
    if axschoice == 'temp':
        plt.figure("Scatter Plot (Hires vs Temp)")
        plt.title(f"Fig name: {name}\nCycle hires vs Temperature ({start_date}-{end_date})",fontsize = 12)
        plt.xlabel('Temperature (celsius)')
    elif axschoice == 'precip':
        plt.figure("Scatter Plot (Hires vs Precip)")
        plt.title(f"Fig name:{name}\nCycle hires vs Precipitation ({start_date}-{end_date})",fontsize = 12)
        plt.xlabel('Precipitation (mm/hr)')
    plt.ylabel('Number of Bicycle Hires')
    plt.scatter(x,y)
    plt.savefig(filepath)
    plt.close()

def line_of_best_fit_plot(name,x,y,axschoice,start_date,end_date,filepath):
    #function adapted from own cw1 comp0035
    if axschoice == 'temp':
        plt.figure("Best Fit Line Plot (Hires vs Temp)")
        plt.title(f"Fig name: {name}\nCycle hires vs Temperature ({start_date}-{end_date})",fontsize = 12)
        plt.xlabel('Temperature (celsius)')
    elif axschoice == 'precip':
        plt.figure("Best Fit Line Plot (Hires vs Precip)")
        plt.title(f"Fig name: {name}\nCycle hires vs Precipitation ({start_date}-{end_date})",fontsize = 12)
        plt.xlabel('Precipitation (mm/hr)')
    plt.ylabel('Number of Bicycle Hires')

    #Coefficients of line of best fit using linear regression
    cfts = np.polyfit(x,y,1)
    line_equation = np.poly1d(cfts)
    #set temperature range between min and max over dates examined, split over 1000 points
    temp_range = np.linspace(-3.2,30.3,1000)
    plt.plot(temp_range,line_equation(temp_range))
    plt.savefig(filepath)
    plt.close()



def extract_column_as_list(data, column_name):
    column_values = [entry[column_name] for entry in data]
    return column_values


def filter_json_data_by_date(data, start_date, end_date):
    # Convert start_date and end_date strings to datetime objects
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')

    # Filter based on date range passed to function
    filtered_data = [
        entry for entry in data 
        if datetime.datetime.strptime(entry['date'], '%d/%m/%Y') >= start_date
        and datetime.datetime.strptime(entry['date'], '%d/%m/%Y') <= end_date
    ]

    return filtered_data


def buildChart(name,start_date,end_date,data_type,plot_type,filepath,cycling_data):
    #filter data based on user input
    date_specific_data = filter_json_data_by_date(cycling_data,start_date,end_date)
    y = extract_column_as_list(date_specific_data,"NumBicylces")
    if data_type:
        x = extract_column_as_list(date_specific_data,"temp")
        x_axis = "temp"
    else:
        x = extract_column_as_list(date_specific_data,"precip")
        x_axis = "precip"
    if plot_type:
        scatter_plot(name,x,y,x_axis,start_date,end_date,filepath)
    else:
        line_of_best_fit_plot(name,x,y,x_axis,start_date,end_date,filepath)

    if plot_type:
        if data_type:
            x = extract_column_as_list(date_specific_data,"temp")
            scatter_plot(name,x,y,'temp',start_date,end_date,filepath)
        else:
            x = extract_column_as_list(date_specific_data,"precip")
            scatter_plot(name,x,y,'precip',start_date,end_date,filepath)
    else:
        #create best fit line plot
        pass


