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

|----------|


## Part 1: Analyze and Explore the Climate Data
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

## Part 1A: Exploratory Precipitation Analysis

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

- This data was then compiled into two lists and then into a DataFrame (using [Pandas](https://pandas.pydata.org/docs/), where it was sorted and NaN precipitation values were cleaned:<br/>

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

|----------------|
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

``<br/>
``<br/>
``<br/>
``<br/>
``<br/>
``<br/>
---


Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:

List the stations and observation counts in descending order.

HINT
Answer the following question: which station id has the greatest number of observations?
Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

HINT
Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:

Filter by the station that has the greatest number of observations.

Query the previous 12 months of TOBS data for that station.

Plot the results as a histogram with bins=12, as the following image shows:

A screenshot depicts the histogram.
Close your session.

Part 2: Design Your Climate App
Now that you???ve completed your initial analysis, you???ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:

/

Start at the homepage.

List all the available routes.

/api/v1.0/precipitation

Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

Return the JSON representation of your dictionary.

/api/v1.0/stations

Return a JSON list of stations from the dataset.
/api/v1.0/tobs

Query the dates and temperature observations of the most-active station for the previous year of data.

Return a JSON list of temperature observations for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>

Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

Hints
Join the station and measurement tables for some of the queries.

Use the Flask jsonify function to convert your API data to a valid JSON response object.
