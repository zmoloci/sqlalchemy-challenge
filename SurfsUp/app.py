import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/precipitation_b<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # extract most recent date by sorting dates in descending order and returning the first value
    recent_date = session.query(Measure).order_by(
        (Measure.date).desc()).first()
    recent_date.date

    # Design a query to retrieve the last 12 months of precipitation data and plot the results.
    # Starting from the most recent data point in the database.

    # Calculate the date one year from the last date in data set.
    yr_ago = (dt.strptime(recent_date.date, '%Y-%m-%d')) + \
        relativedelta(years=-1)

    # Perform a query to retrieve the data and precipitation scores
    last_yr_precip = session.query(Measure).filter(
        Measure.date >= yr_ago).order_by((Measure.date).desc()).all()

    # Close session
    session.close


# Build lists for date and prcp values
    measuredate = []
    precip = []

    for row in last_yr_precip:
        measuredate.append(row.date)
        precip.append(row.prcp)

# Build dictionary with unique dates as the key and since each date has multiple measurements,
# value will be lists of precipitation measurements
    precip_dict = {}
    valuelist = []
    for i in range(len(last_yr_precip)):
        if i > 0:
            if measuredate[i] == measuredate[i-1]:
                valuelist.append(precip[i])
            else:
                precip_dict[f'{measuredate[i-1]}'] = valuelist
                valuelist = []
        else:
            valuelist.append(precip[i])

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations (including id, station, name, latitude, longitude, elevation)
    results = session.query(Station.id, Station.station, Station.name, Station.latitude,
                            Station.longitude, Station.elevation)

    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list
    all_stations = []
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation_b")
def precipitation_b():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # extract most recent date by sorting dates in descending order and returning the first value
    recent_date = session.query(Measure).order_by(
        (Measure.date).desc()).first()
    recent_date.date

    # Design a query to retrieve the last 12 months of precipitation data and plot the results.
    # Starting from the most recent data point in the database.

    # Calculate the date one year from the last date in data set.
    yr_ago = (dt.strptime(recent_date.date, '%Y-%m-%d')) + \
        relativedelta(years=-1)

    # Perform a query to retrieve the data and precipitation scores
    last_yr_precip = session.query(Measure).filter(
        Measure.date >= yr_ago).order_by((Measure.date).desc()).all()

    session.close

    measuredate = []
    precip = []

    for row in last_yr_precip:
        # print(row.date, row.prcp)
        measuredate.append(row.date)
        precip.append(row.prcp)

    # Save the query results as a Pandas DataFrame and set the index to the date column
    last_yr_precip_df = pd.DataFrame({'Date': measuredate,
                                      'Precipitation': precip}).set_index('Date')

    # Sort the dataframe by date
    last_yr_precip_df.sort_index(inplace=True)

    # Remove rows with NaN prcp values and print df
    clean_last_year = last_yr_precip_df.dropna()

    # Groupby 'Date' and print df
    gb = clean_last_year.groupby(
        'Date')['Precipitation'].sum().reset_index(name='Precipitation')

    clean_meas_date = gb['Date'].to_list()
    clean_precip = gb['Precipitation'].to_list()

    # clean_meas_date = []
    # clean_precip = []

    precip_dict = {}
    for date in clean_meas_date:
        for value in clean_precip:
            precip_dict[date] = value
            precip.remove(value)
            break

    return jsonify(precip_dict)


if __name__ == '__main__':
    app.run(debug=True)
