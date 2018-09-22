# SQLalchemy - weather
wk11-HW

With this assignment I created a climate analysis API that "predicts" weather based on previous weather. I was provided two CSV files containing the data and used Pandas, Numpy, MatPlotLib, and Seaborn for analysis and visualizations, SQLAlchemy to connect to an SQLite database created from the cleaned CSVs, and Flask to generate a mini-API.

I used an ORM to map the data from the CSV files into my sqlite database then created a session link to connect my python file to the database so I could run queries. I queried weather data for the last twelve months, primarily temperature and precipitation, then created functions to accept a start and end date (for an upcoming trip, for example) which returned the low, high and average temperature; and precipitation measurements for each weather station in the area for that time period, based off of the previous year’s data. All these queries were put into individual routes of a Flask-API, returning a JSON list of the results.

![rain in HI](hawaii_rainStation.pgn?raw=true "Optional Title")
