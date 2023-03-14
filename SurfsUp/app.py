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
    # included some additional information re: each route here. This is especially helpful in defining the format
    # of the last two routes.
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"(returns each precipitation value for each date over last 12 months of the dataset. Note not all stations have a measurement for each date so the number of values per date is variable.)<br/><br/>"
        f"/api/v1.0/sumprecipitation<br/>"
        f"(returns daily sum of precipitation across all stations by date over last 12 months of the dataset)<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"(returns elevation, id, latitude, longitude, name and station codes)<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"(includes daily temperature values by date for most active station over last 12 months of the dataset)<br/><br/>"
        f"/api/v1.0/start/<b>'start'</b><br/>"
        f"(replace <b>'start'</b> with date in format <b>yyyy-mm-dd</b><br/>"
        f"returns minimum, average and max temperature for date range starting with specified date)<br/><br/>"
        f"/api/v1.0/start_end/<b>'start_end'</b><br/>"
        f"(replace <b>'start_end'</b> with date range in format <b>yyyy-mm-dd-yyyy-mm-dd</b><br/>"
        f"returns minimum, average and max temperature for date range specified)<br/><br/>"
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


@app.route("/api/v1.0/sumprecipitation")
def sumprecipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Then, extract most recent date by sorting dates in descending order and returning the first value
    recent_date = session.query(Measure).order_by(
        (Measure.date).desc()).first()
    recent_date.date

   # Calculate the date one year from the last date in data set.
    yr_ago = (dt.strptime(recent_date.date, '%Y-%m-%d')) + \
        relativedelta(years=-1)

    # Perform a query to retrieve the data and precipitation scores
    last_yr_precip = session.query(Measure).filter(
        Measure.date >= yr_ago).order_by((Measure.date).desc()).all()
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
        'Date')['Precipitation'].sum().round(2).reset_index(name='Precipitation')

    # Use dictionary comprehension to build dateprecip dictionary from gb dataframe
    dateprecip = {gb['Date'].to_list()[i]: gb['Precipitation'].to_list()[i]
                  for i in range(len(gb['Date'].to_list()))}

    return jsonify(dateprecip)


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


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and temperature (tobs) observations for most-active station for the
    # previous year of data

    # Sort Measure data by descending date and filter to most active station (USC00519281)
    # Return most recent date for station (in case station has different most recent measurement)
    recent_USC00519281_date = session.query(Measure).order_by((Measure.date).desc())\
        .filter(Measure.station == "USC00519281").first()

    # Calculate the date one year from the last date in data set for station USC00519281.
    yr_ago = (dt.strptime(recent_USC00519281_date.date, '%Y-%m-%d')) + \
        relativedelta(years=-1)

    # Perform query for last year of data for station USC00519281
    last_yr_temp = session.query(Measure).filter(Measure.date >= yr_ago)\
        .filter(Measure.station == "USC00519281").order_by((Measure.date).desc()).all()

    # Close session
    session.close()

    # Build list of dictionaries
    USC00519281_data = []
    for row in last_yr_temp:
        station_data = {}
        station_data["date"] = row.date
        station_data["temperature"] = row.tobs
        USC00519281_data.append(station_data)

    return jsonify(USC00519281_data)


@app.route("/api/v1.0/start/<start>")
def temp_analysis_start(start):
    """ Fetch min, avg and temperature for range starting with start date
    supplied by the user"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations (including id, station, name, latitude, longitude, elevation)
    results = session.query(Station.id, Station.station, Station.name,
                            Station.latitude, Station.longitude, Station.elevation)

    # Create empty list to be populated with dictionaries
    range_data = []

    # Define function for TMIN, TAVG, TMAX from tobs data in Measure
    sel = [func.min(Measure.tobs),
           func.avg(Measure.tobs),
           func.max(Measure.tobs)]

    # Build dictionary of station info and temperature statistics as outlined in the above function
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_stats = []
        station_stats = session.query(*sel).\
            filter(Measure.date >= start).\
            filter(Measure.station == station).all()
        station_dict["TMIN"] = station_stats[0][0]
        station_dict["TAVG"] = station_stats[0][1]
        station_dict["TMAX"] = station_stats[0][2]
    # append dictionary to list "range_data" created above
        range_data.append(station_dict)

    # close session and return range_data in json format
    session.close()
    return jsonify(range_data)


@app.route("/api/v1.0/start_end/<start_end>")
def temp_analysis_startend(start_end):
    """ Fetch min, avg and temperature for range starting with start date
    supplied by the user"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # split user input into start and end dates as per format defined on the main page (yyyy-mm-dd_yyyy-mm-dd)
    start = start_end[:10]
    end = start_end[-10:]

    # Query all stations (including id, station, name, latitude, longitude, elevation)
    results = session.query(Station.id, Station.station, Station.name,
                            Station.latitude, Station.longitude, Station.elevation)

    # Create empty list to be populated
    range_data = []

    # Define function for TMIN, TAVG, TMAX from tobs data in Measure
    sel = [func.min(Measure.tobs),
           func.avg(Measure.tobs),
           func.max(Measure.tobs)]

    # Build dictionary of station info and temperature statistics as outlined in the above function
    for id, station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_stats = []
        station_stats = session.query(*sel).\
            filter(Measure.date <= end).\
            filter(Measure.date >= start).\
            filter(Measure.station == station).all()
        station_dict["TMIN"] = station_stats[0][0]
        station_dict["TAVG"] = station_stats[0][1]
        station_dict["TMAX"] = station_stats[0][2]
        # append dictionary to list "range_data" created above
        range_data.append(station_dict)

    # close session and return range_data in json format
    session.close()
    return jsonify(range_data)


if __name__ == '__main__':
    app.run(debug=True)
