# sqlalchemy-challenge
### Module 10 Challenge

#### Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that taken to accomplish this task.

## First steps:

- Created [this repository](https://github.com/zmoloci/sqlalchemy-challenge) for the project.

- This was then cloned to my workstation.

- Inside [this repository](https://github.com/zmoloci/sqlalchemy-challenge), the [SurfsUp](https://github.com/zmoloci/sqlalchemy-challenge/tree/main/SurfsUp) directory was created to house the [Resources folder](https://github.com/zmoloci/sqlalchemy-challenge/tree/main/SurfsUp/Resources), [Jupyter notebook (climate_starter.ipynb)](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb) and [Flask](https://flask.palletsprojects.com/en/2.2.x/) [app file (app.py)](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/app.py).

- The [Jupyter notebook (climate_starter.ipynb)](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/climate_starter.ipynb) and [app file (app.py)](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/app.py) contain the main scripts to run for analysis.
- The [Resources folder](https://github.com/zmoloci/sqlalchemy-challenge/tree/main/SurfsUp/Resources) contains the data files ([hawaii.sqlite](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii.sqlite), [hawaii_measurements.csv](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii_measurements.csv) and [hawaii_stations.csv](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii_stations.csv)) used for this challenge.

- Changes were regularly pushed to [GitHub](https://github.com/zmoloci/sqlalchemy-challenge).

---


# Part 1: Analyze and Explore the Climate Data
In this section, Python and SQLAlchemy are used to do a basic climate analysis and data exploration of your climate database. Specifically, SQLAlchemy ORM queries, Pandas, and Matplotlib were used to complete the following steps:

- The provided [hawaii.sqlite](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii.sqlite) was used to complete the climate analysis and data exploration.

- SQLAlchemy create_engine() function was used  to connect to the SQLite database ([hawaii.sqlite](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/SurfsUp/Resources/hawaii.sqlite)).<br/>

`engine = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)`

- The SQLAlchemy automap_base() function was used to reflect tables into classes, and then references were saved to the classes named station and measurement.<br/>

`Base = automap_base()`<br/>
`Base.prepare(autoload_with=engine)`<br/>
`Base.classes.keys()`<br/>
`Measure = Base.classes.measurement`<br/>
`Station = Base.classes.station`<br/>



- Python was then linked to the database by creating a SQLAlchemy session.<br/>

`session = Session(engine)`

# Part 1A: Exploratory Precipitation Analysis

A precipitation analysis and then a station analysis were performed by completing the steps in the following two subsections.
---
### Precipitation Analysis
---
### Find the most recent date in the dataset:
- First, the column headers in the Measure dataset were displayed:

`first_row = session.query(Measure).first()`<br/>
`first_row.__dict__`

- An alternate method using [sqlalchemy.inspection](https://www.fullstackpython.com/sqlalchemy-inspection-inspect-examples.html) to examine the column headers as well as data types was also displayed:<br/>

`inspector = inspect(engine)`<br/>

`for tables in inspector.get_table_names():`<br/>
    `print(f"'{tables}' column headers (TYPE):")`<br/>
    `print("    ")`<br/>
    `columns = inspector.get_columns(tables)`<br/>
    `for c in columns:`<br/>
    `   print(f'{c["name"]} ({c["type"]})')`<br/>
    `print("----------------")`<br/>
    `print("   ")`<br/>

- The most recent date was then retrieved, by sorting the Measure dataset by the date in descending order and displaying the first date:<br/>

`recent_date = session.query(Measure).order_by((Measure.date).desc()).first()`<br/>
`recent_date.date`<br/>

---
- Using that date, the previous 12 months of precipitation data were retrieved by querying the previous 12 months of data.

- First the date for 12 months before the most recent data was calculated:<br/>

`yr_ago = (dt.strptime(recent_date.date, '%Y-%m-%d'))+relativedelta(years=-1)`<br/>

- Then a query was performed to retrieve date and precipitation values:<br/>

`last_yr_precip = session.query(Measure).filter(Measure.date >= yr_ago).order_by((Measure.date).desc()).all()`<br/>

- This data was then compiled into two lists and then into a DataFrame (using [Pandas](https://pandas.pydata.org/docs/)), where it was sorted and NaN precipitation values were cleaned:<br/>

`measuredate=[]`<br/>
`precip=[]`<br/>

`for row in last_yr_precip:`<br/>
`    measuredate.append(row.date)`<br/>
`    precip.append(row.prcp)`<br/>

`last_yr_precip_df = pd.DataFrame({'Date': measuredate,`<br/>
`    'Precipitation':precip}).set_index('Date')`<br/>

`last_yr_precip_df.sort_index(inplace=True)`<br/>

`clean_last_year = last_yr_precip_df.dropna()`<br/>
`print(clean_last_year)`<br/>

- The precipitation values were then summed across all stations for each date:<br/>
`gb=clean_last_year.groupby('Date')['Precipitation'].sum().reset_index(name='Precipitation')`<br/>

- and the frequencies of each temperature value were plotted by ascending date using Pandas Plotting with Matplotlib:<br/>
`fig, ax = plt.subplots()`<br/>
`ax.bar(gb['Date'],gb['Precipitation'])`<br/>
`plt.xlabel("Date")`<br/>
`plt.ylabel("inches")`<br/>
`plt.xticks(np.arange(0,len(gb['Date']),29.5),rotation=90)`<br/>
`plt.legend(['Precipitation'])`<br/>
`plt.show()`<br/>


![1-year precipitation data across all stations](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/Figures/fig1.png)
|----------------|

<br/>
- Then the 1-year precipitation data was analyzed using [pandas.describe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html) and summary statistics were displayed:<br/>
`gb.describe()`<br/>

---
## Part 1B: Exploratory Station Analysis

---
### Station Analysis


- First the Measure data was queried in order to calculate the total number of stations in the dataset:<br/>
`len(session.query(Station.station).group_by(Station.station).all())`<br/>


---


### Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:


### List the stations and observation counts in descending order.

Answer the following question: which station id has the greatest number of observations?<br/>
`station_activity = session.query(Measure).all()`<br/>

`id=[]`<br/>
`station=[]`<br/>
`temp=[]`<br/>

`for row in station_activity:`<br/>
`    id.append(row.id)`<br/>
`    station.append(row.station)`<br/>
`    temp.append(row.tobs)`<br/>

`station_activity_df = pd.DataFrame({'id': id,'station code':station,'temp':temp}).set_index('id')`<br/>

- Sort the dataframe by date <br/>
`station_activity_df.sort_index(inplace=True)`<br/>

- Remove rows with NaN prcp values and print df<br/>
`clean_station = station_activity_df.dropna()`<br/>


- Groupby 'Date' and print df<br/>
`gbstat=clean_station.groupby('station code')['temp'].count().reset_index(name='entry count').sort_values(by=['entry count'],ascending=False)`<br/>
`bstats=gbstat.reset_index(drop=True)`<br/>
`print(gbstats)`<br/>
<br/>

| ![fig.2 - Stations by Observation Count (Descending)](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/Figures/fig2.png)|
| ----------- |

<br/>
---
A query was designed that calculates the lowest, highest, and average temperatures and filters on the most-active station id found in the previous query.

`sel = [Measure.station,`<br/>
       `func.min(Measure.tobs),`<br/>
       `func.max(Measure.tobs),`<br/>
       `func.avg(Measure.tobs)]`<br/>
`USC00519281_temp_stats = session.query(*sel).\`<br/>
    `filter(Measure.station == "USC00519281").all()`<br/>
`USC00519281_temp_stats`<br/>

---

A query was designed to get the previous 12 months of temperature observation (TOBS) data by following these steps:

- Filter by the station that has the greatest number of observations, sort by descending date and then return the most recent (first) date<br/>
`recent_USC00519281_date = session.query(Measure).order_by((Measure.date).desc()).filter(Measure.station == "USC00519281").first()`<br/>
`recent_USC00519281_date.date`<br/>

- Calculate the date one year from the last date in the data set<br/>

  `yr_ago = (dt.strptime(recent_USC00519281_date.date, '%Y-%m-%d'))+relativedelta(years=-1)`<br/>

- Query the previous 12 months of TOBS data for that station.<br/>
  `last_yr_temp = session.query(Measure).filter(Measure.date >= yr_ago).filter(Measure.station == "USC00519281").order_by((Measure.date).desc()).all()`<br/>

  `stationname = []`<br/>
  `tempmeasuredate=[]`<br/>
  `temp=[]`<br/>

  `for row in last_yr_temp:`<br/>
      `# print(row.station,row.date, row.tobs)`<br/>
      `stationname.append(row.station)`<br/>
      `tempmeasuredate.append(row.date)`<br/>
      `temp.append(row.tobs)`<br/>


- Sort the dataframe by date
`last_yr_USC00519281_temp_df = pd.DataFrame({'Date': tempmeasuredate,`<br/>
                                 `'Temperature':temp})`<br/>
`last_yr_USC00519281_temp_df.sort_index(inplace=True)`<br/>

- Drop NaN temp measurements
`clean_last_year_temp = last_yr_USC00519281_temp_df.dropna()`<br/>

- Groupby on Temperature values to give number of days at each temperature over 12 month period
`gbt=clean_last_year_temp.groupby('Temperature')['Date'].count().reset_index(name='Days')`<br/>
`print(gbt)`<br/>

<br/>

| ![fig.3 - Frequency of Temperature Readings by Degrees Farenheit](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/Figures/fig3.png)|
| ----------- |

<br/>

- Plot the results as a histogram with bins=12, as the following image shows:<br/>
- Created 12 equal width bins on temperature using min, max values<br/>
`bins = []`<br/>
`labels = []`<br/>
`for i in range(0,13):`<br/>
    `bins.append((min(gbt['Temperature'])-.01) + (i*(((max(gbt['Temperature'])+.01)-min(gbt['Temperature']))/12)))`<br/>
    `if i != 0:`<br/>
        `labels.append(f'{bins[i-1]:.1f}-{bins[i]:.1f}')`<br/>
`gbt['bin'] = pd.cut(gbt['Temperature'], bins=bins, labels=labels)`<br/>

- Groupby on bins<br/>
`gbt_binned = gbt.groupby('bin')['Days'].sum().reset_index(name='Days')`<br/>
`gbt_binned.columns = ['Temperature','Days']`<br/>
`print(gbt_binned)`<br/>

- Plot frequency of temperature readings as histogram including xlabel, ylabel and legend<br/>
`fig, ax = plt.subplots()`<br/>
`ax.bar(gbt_binned['Temperature'],gbt_binned['Days'])`<br/>
`plt.xlabel("Temperature (Degrees Farenheit)")`<br/>
`plt.ylabel("Number of Days")`<br/>
`plt.xticks(np.arange(0,13,1),rotation=90)`<br/>
`plt.legend(['tobs'])`<br/>
`plt.show()`<br/>

<br/>

| ![fig.4 - Histogram of Temperature Readings by Degrees Farenheit](https://github.com/zmoloci/sqlalchemy-challenge/blob/main/Figures/fig4.png)|
| ----------- |

<br/>
- Close the session<br/>

`session.close()`<br/>



# Part 2: Design Your Climate App
## Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

### `/`<br/>

### Start at the homepage.

### List all the available routes.

```
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

```


### `/api/v1.0/precipitation`<br/>

### Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

### Return the JSON representation of your dictionary.

```
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

```

### An alternate route for precipitation data:
### returns daily sum of precipitation across all stations by date over last 12 months of the dataset
### `/api/v1.0/sumprecipitation`<br/>

```
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
    
```


### `/api/v1.0/stations`<br/>

### Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")

```
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
```


### `/api/v1.0/tobs`<br/>

### Query the dates and temperature observations of the most-active station for the previous year of data.

### Return a JSON list of temperature observations for the previous year.

```
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
```

### `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  
### Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

### For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.


```
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

```
    
    
### For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
```
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
```

## Set entry point for program<br/>
```
if __name__ == '__main__':
    app.run(debug=True)
```
