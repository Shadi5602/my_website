#adapted from COMP0034 week 2 tutorial.
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.logger.info(f"Starting app from tfl_REST")
    app.config.from_mapping(
        SECRET_KEY='RB3M2sQk7gLaMrsUtGiEVg',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'tfl_rest_flask.sqlite'),
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

    #activate below with names of models from my data sets
    from tfl_restapi_flask.models import User, CyclingAndWeather

    with app.app_context():
        db.create_all()
        #activate below when add_data_from_csv function is ready for use
        add_data_from_csv()
        from tfl_restapi_flask import routes
        
    return app

import csv
from pathlib import Path

def add_data_from_csv():
    """Adds data to the database if it does not already exist."""

    # Add import here and not at the top of the file to avoid circular import issues
    from tfl_restapi_flask.models import CyclingAndWeather

    # If there are no rows in the database, then add them
    first_data = db.session.execute(db.select(CyclingAndWeather)).first()
    if not first_data:
        print("Start adding weather and cycling data to the database")
        data_file = Path(__file__).parent.parent.joinpath("data", "dataset_prepared.csv")
        with open(data_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # row[0] is the first column, row[1] is the second column
                r = CyclingAndWeather(date=row[0], temp=row[1], precip=row[2], NumBicylces = row[3])
                db.session.add(r)
            db.session.commit()



    from tfl_restapi_flask.models import SavedCharts
    first_chart = db.session.execute(db.select(SavedCharts)).first()
    if not first_chart:
        print("Start adding saved chart to the database from csv")
        data_file = Path(__file__).parent.parent.joinpath("data", "SavedCharts.csv")
        with open(data_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # row[0] is the first column, row[1] is the second column
                r = SavedCharts(name = row[0], user_id=row[1], start_date=row[2],end_date=row[3],data_type=row[4],plot_type=row[5])
                db.session.add(r)
            db.session.commit()

        
     # Add import here and not at the top of the file to avoid circular import issues
    from tfl_restapi_flask.models import User

    # If there are no rows in the database, then add them
    first_user = db.session.execute(db.select(User)).first()
    if not first_user:
        print("Start adding user data to the database")
        data_file_user = Path(__file__).parent.parent.joinpath("data", "UserData.csv")
        with open(data_file_user, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                # row[0] is the first column, row[1] is the second column
                r = User(row[0],row[1],row[2])
                db.session.add(r)
            db.session.commit()