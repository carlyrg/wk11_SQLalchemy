

```python
%matplotlib notebook
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import seaborn as sns
```


```python
import numpy as np
import pandas as pd
```


```python
import datetime as dt
```


```python
from flask import Flask, jsonify, render_template
import json
import requests
from flask import request
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

%ls
```

     Volume in drive C is Windows
     Volume Serial Number is 4A49-EB92
    
     Directory of C:\Users\snowr\ds_python1\HOMEWORK\wk11_SQL
    
    07/27/2018  07:46 PM    <DIR>          .
    07/27/2018  07:46 PM    <DIR>          ..
    07/27/2018  06:24 PM    <DIR>          .ipynb_checkpoints
    07/27/2018  06:18 PM           573,585 clean_hawaii_measurements.csv
    07/27/2018  06:19 PM               628 clean_hawaii_stations.csv
    07/27/2018  07:43 PM             3,537 climate_analysis.ipynb
    07/27/2018  07:44 PM           390,988 climate_analysis_cg.ipynb
    07/27/2018  07:43 PM            18,960 data_engineering.ipynb
    07/27/2018  07:43 PM             8,116 database_engineering.ipynb
    07/27/2018  07:35 PM           745,472 hawaii.sqlite
    07/26/2018  05:48 PM    <DIR>          Images
    07/26/2018  05:20 PM             6,522 README.md
    07/26/2018  05:48 PM    <DIR>          Resources
                   8 File(s)      1,747,808 bytes
                   5 Dir(s)  269,079,089,152 bytes free
    


```python
engine = create_engine("sqlite:///hawaii.sqlite")
```


```python
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
```


```python
# We can view all of the classes that automap found
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
```


```python
# Create our session (link) from Python to the DB
session = Session(engine)
```


```python
pd.read_sql("""SELECT * FROM station""", engine.connect()).head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.2716</td>
      <td>-157.8168</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.4234</td>
      <td>-157.8015</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.5213</td>
      <td>-157.8374</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.3934</td>
      <td>-157.9751</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.4992</td>
      <td>-158.0111</td>
      <td>306.6</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.read_sql("""SELECT * FROM measurement""", engine.connect()).head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00519397</td>
      <td>2010-01-06</td>
      <td>NaN</td>
      <td>73.0</td>
    </tr>
  </tbody>
</table>
</div>



# Exploratory Climate Analysis


```python
today = pd.datetime.today().date()
begin = today - pd.offsets.Day(365)
date_range = pd.date_range(begin, today)

measurement = pd.read_sql("""SELECT * FROM measurement""", engine.connect())
measurement['date'] = pd.to_datetime(measurement['date'], format = '%Y-%m-%d')
measurement[measurement.date > dt.datetime.now() - pd.to_timedelta("365day")]
dates = (measurement['date'] >= begin) & (measurement['date'] <= today)
ytd_measure = measurement.loc[dates].fillna(0)
ytd_measure.sample(15)

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>12177</th>
      <td>12178</td>
      <td>USC00519523</td>
      <td>2017-08-12</td>
      <td>0.00</td>
      <td>83.0</td>
    </tr>
    <tr>
      <th>2698</th>
      <td>2699</td>
      <td>USC00519397</td>
      <td>2017-07-27</td>
      <td>0.00</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>2714</th>
      <td>2715</td>
      <td>USC00519397</td>
      <td>2017-08-12</td>
      <td>0.00</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>2711</th>
      <td>2712</td>
      <td>USC00519397</td>
      <td>2017-08-09</td>
      <td>0.00</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>12176</th>
      <td>12177</td>
      <td>USC00519523</td>
      <td>2017-08-11</td>
      <td>0.00</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>14950</th>
      <td>14951</td>
      <td>USC00519281</td>
      <td>2017-08-04</td>
      <td>0.00</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2712</th>
      <td>2713</td>
      <td>USC00519397</td>
      <td>2017-08-10</td>
      <td>0.00</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>7625</th>
      <td>7626</td>
      <td>USC00514830</td>
      <td>2017-08-13</td>
      <td>0.00</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>9006</th>
      <td>9007</td>
      <td>USC00517948</td>
      <td>2017-07-31</td>
      <td>0.00</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>14953</th>
      <td>14954</td>
      <td>USC00519281</td>
      <td>2017-08-13</td>
      <td>0.00</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>19541</th>
      <td>19542</td>
      <td>USC00516128</td>
      <td>2017-08-15</td>
      <td>0.42</td>
      <td>70.0</td>
    </tr>
    <tr>
      <th>12170</th>
      <td>12171</td>
      <td>USC00519523</td>
      <td>2017-08-03</td>
      <td>0.00</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>7619</th>
      <td>7620</td>
      <td>USC00514830</td>
      <td>2017-08-06</td>
      <td>0.00</td>
      <td>82.0</td>
    </tr>
    <tr>
      <th>19533</th>
      <td>19534</td>
      <td>USC00516128</td>
      <td>2017-08-07</td>
      <td>0.05</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>2706</th>
      <td>2707</td>
      <td>USC00519397</td>
      <td>2017-08-04</td>
      <td>0.02</td>
      <td>80.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
stations_df = pd.read_sql("""SELECT * FROM station""", engine.connect())
stations_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.52130</td>
      <td>-157.83740</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.39340</td>
      <td>-157.97510</td>
      <td>11.9</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.49920</td>
      <td>-158.01110</td>
      <td>306.6</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>21.33556</td>
      <td>-157.71139</td>
      <td>19.5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>7</td>
      <td>USC00519281</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>USC00511918</td>
      <td>HONOLULU OBSERVATORY 702.2, HI US</td>
      <td>21.31520</td>
      <td>-157.99920</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>USC00516128</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Design a query to retrieve the last 12 months of precipitation data and plot the results
merge_data = pd.read_sql ("""SELECT m.date, m.station, m.prcp, m.tobs, s.name, s.latitude, s.longitude, s.elevation
            FROM measurement AS m
            JOIN station AS s ON s.station = m.station""", engine.connect())
merge_data['date'] = pd.to_datetime(merge_data['date'], format = '%Y-%m-%d')
months12 = (merge_data['date'] >= begin) & (merge_data['date'] <= today)
ytd = merge_data.loc[months12].fillna(0)
ytd

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>station</th>
      <th>prcp</th>
      <th>tobs</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2698</th>
      <td>2017-07-27</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>79.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2699</th>
      <td>2017-07-28</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2700</th>
      <td>2017-07-29</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2701</th>
      <td>2017-07-30</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2702</th>
      <td>2017-07-31</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2703</th>
      <td>2017-08-01</td>
      <td>USC00519397</td>
      <td>0.02</td>
      <td>77.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2704</th>
      <td>2017-08-02</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>73.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2705</th>
      <td>2017-08-03</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>79.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2706</th>
      <td>2017-08-04</td>
      <td>USC00519397</td>
      <td>0.02</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2707</th>
      <td>2017-08-05</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2708</th>
      <td>2017-08-06</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2709</th>
      <td>2017-08-07</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2710</th>
      <td>2017-08-08</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2711</th>
      <td>2017-08-09</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2712</th>
      <td>2017-08-10</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2713</th>
      <td>2017-08-11</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>78.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2714</th>
      <td>2017-08-12</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2715</th>
      <td>2017-08-13</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2716</th>
      <td>2017-08-14</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>79.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2717</th>
      <td>2017-08-15</td>
      <td>USC00519397</td>
      <td>0.02</td>
      <td>78.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2718</th>
      <td>2017-08-18</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2719</th>
      <td>2017-08-19</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>79.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2720</th>
      <td>2017-08-20</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2721</th>
      <td>2017-08-21</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2722</th>
      <td>2017-08-22</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>82.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2723</th>
      <td>2017-08-23</td>
      <td>USC00519397</td>
      <td>0.00</td>
      <td>81.0</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>5428</th>
      <td>2017-07-27</td>
      <td>USC00513117</td>
      <td>0.00</td>
      <td>77.0</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>5429</th>
      <td>2017-07-28</td>
      <td>USC00513117</td>
      <td>0.13</td>
      <td>77.0</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>5430</th>
      <td>2017-07-29</td>
      <td>USC00513117</td>
      <td>0.06</td>
      <td>78.0</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>5431</th>
      <td>2017-07-30</td>
      <td>USC00513117</td>
      <td>0.00</td>
      <td>78.0</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>14956</th>
      <td>2017-08-16</td>
      <td>USC00519281</td>
      <td>0.12</td>
      <td>76.0</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>14957</th>
      <td>2017-08-17</td>
      <td>USC00519281</td>
      <td>0.01</td>
      <td>76.0</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>14958</th>
      <td>2017-08-18</td>
      <td>USC00519281</td>
      <td>0.06</td>
      <td>79.0</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>19523</th>
      <td>2017-07-27</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>75.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19524</th>
      <td>2017-07-28</td>
      <td>USC00516128</td>
      <td>0.40</td>
      <td>73.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19525</th>
      <td>2017-07-29</td>
      <td>USC00516128</td>
      <td>0.30</td>
      <td>77.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19526</th>
      <td>2017-07-30</td>
      <td>USC00516128</td>
      <td>0.30</td>
      <td>79.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19527</th>
      <td>2017-07-31</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>74.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19528</th>
      <td>2017-08-01</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>72.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19529</th>
      <td>2017-08-02</td>
      <td>USC00516128</td>
      <td>0.25</td>
      <td>80.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19530</th>
      <td>2017-08-03</td>
      <td>USC00516128</td>
      <td>0.06</td>
      <td>76.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19531</th>
      <td>2017-08-05</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>77.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19532</th>
      <td>2017-08-06</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>79.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19533</th>
      <td>2017-08-07</td>
      <td>USC00516128</td>
      <td>0.05</td>
      <td>78.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19534</th>
      <td>2017-08-08</td>
      <td>USC00516128</td>
      <td>0.34</td>
      <td>74.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19535</th>
      <td>2017-08-09</td>
      <td>USC00516128</td>
      <td>0.15</td>
      <td>71.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19536</th>
      <td>2017-08-10</td>
      <td>USC00516128</td>
      <td>0.07</td>
      <td>75.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19537</th>
      <td>2017-08-11</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>72.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19538</th>
      <td>2017-08-12</td>
      <td>USC00516128</td>
      <td>0.14</td>
      <td>74.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19539</th>
      <td>2017-08-13</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>80.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19540</th>
      <td>2017-08-14</td>
      <td>USC00516128</td>
      <td>0.22</td>
      <td>79.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19541</th>
      <td>2017-08-15</td>
      <td>USC00516128</td>
      <td>0.42</td>
      <td>70.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19542</th>
      <td>2017-08-16</td>
      <td>USC00516128</td>
      <td>0.42</td>
      <td>71.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19543</th>
      <td>2017-08-17</td>
      <td>USC00516128</td>
      <td>0.13</td>
      <td>72.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19544</th>
      <td>2017-08-18</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>76.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19545</th>
      <td>2017-08-19</td>
      <td>USC00516128</td>
      <td>0.09</td>
      <td>71.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19546</th>
      <td>2017-08-20</td>
      <td>USC00516128</td>
      <td>0.00</td>
      <td>78.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19547</th>
      <td>2017-08-21</td>
      <td>USC00516128</td>
      <td>0.56</td>
      <td>76.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19548</th>
      <td>2017-08-22</td>
      <td>USC00516128</td>
      <td>0.50</td>
      <td>76.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
    <tr>
      <th>19549</th>
      <td>2017-08-23</td>
      <td>USC00516128</td>
      <td>0.45</td>
      <td>76.0</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
    </tr>
  </tbody>
</table>
<p>123 rows × 8 columns</p>
</div>




```python
# Calculate the date 1 year ago from today
last_year = today - pd.offsets.Day(365)
last_year
```




    Timestamp('2017-07-27 00:00:00')




```python
# Perform a query to retrieve the data and precipitation scores
precip = ytd[['date', 'prcp']].copy()
precip.set_index('date', inplace=True)
precip.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-07-27</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-07-28</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-07-29</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-07-30</th>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2017-07-31</th>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#plot precip for year
sns.set()
precip.plot()
plt.xlabel("Date", fontsize=12)
plt.ylabel('Rain in Inches', fontsize=12)
plt.title("Precipitation Ananlysis YTD", fontsize=14)
plt.legend(['precipitation'], fontsize=10)
plt.xticks( fontsize=10)
plt.yticks(fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAj8AAAGvCAYAAAC0IrTpAAAgAElEQVR4XuxdB3gU1dp+z6TQBKRXJUB2NnQERKpiufaOoNfewIaIgL0XsCMiIuBv74JYsHItgKKIgIBAsrOhSFealICE7Jz/OUMWNyHJzM6emZ2dfPM8PpebPeX73vc7s+9+pzHQQwgQAoQAIUAIEAKEQCVCgFUiX8lVQoAQIAQIAUKAECAEQOKHgoAQIAQIAUKAECAEKhUCJH4qFd3kLCFACBAChAAhQAiQ+KEYIAQIAUKAECAECIFKhQCJn0pFNzlLCBAChAAhQAgQAiR+KAYIAUKAECAECAFCoFIhQOKnUtFNzhIChAAhQAgQAoQAiR+KAUKAECAECAFCgBCoVAiQ+KlUdJOzhAAhQAgQAoQAIUDih2KAECAECAFCgBAgBCoVAiR+KhXd5CwhQAgQAoQAIUAIkPihGCAECAFCgBAgBAiBSoUAiZ9KRTc5SwgQAoQAIUAIEAIkfigGCAFCgBAgBAgBQqBSIUDip1LRTc4SAoQAIUAIEAKEAIkfigFCIAEEVFV9DcAVpZrQAewGsJQx9lwoFPoggS7iqqqq6mrRr6ZpZ1qtmJOT00/X9e8ZYwNCodDUtm3bZhYVFT0IYL2maS9YbUeUU1U1B8B4ABdpmral+G9x2xRPnxWVVVW1E4BFgg9d15vl5+fvlNV2Iu2oqvojgMM0TeucSDuxdYPB4KOc83sKCwvrrF69+u94223evHm16tWrLwDQknPeJRwO55ZuIzs7u7WiKIsZY6FIJHKXoihfW+jnZU3Trg0EAm8xxi4pVX4fgL8AfK8oyqi8vDzNQntUhBBIGAESPwlDSA1UZgSi4kfX9Z5RHNLT0xXOeX3O+UgAfQFcrmnam27glJ2dfVRaWtqeUCgUstpfdnZ2LQBtq1Spoi1btmxbTk5Olq7rqzjnt4XD4aettlMsdIRoegBAg6j4sWNTPH1WVDYQCExgjPUD0JoxdnsoFHpOVtuJtOOE+MnOzm4OoHl+fv6vACJ27MvOzu6iKMpcIRg1TRMxHduOoqrqbACdFUXpUlRUtEnETbSftLS05pzzKYyxSZFIRPwoMB7G2F/hcHhlsfi5SNf1Pv9+xGooitJOjBXGWF0AJ4dCoTl2bKc6hEA8CJD4iQctKksIlEIgKn40TTtkLAWDwZqc87UA1mma1j5VwJMtfpLld8eOHWv8888/GzjnTymK0p1z3kbTNBUAT5ZN0X6dED+yfFJV9W4Aozjn94bD4VHRdoPB4O2c8yc451eHw+FXS/fXunXr7LS0tDDn/L5wOPxo6c+j4kfTtPTSn7Vt27ZxUVHRAsZYUSQSUfPz80VGiB5CwDEESPw4Bi01XBkQqEj8CP9VVf1F/FLWNK1KVFQAEBmhgQDaAHhd07SbxRf1vn37RNZkIOe8MQAhmsR0wZOxv74DgUAbRVEe4ZyLbEYmgMUAHtQ07dvi/kpMMamqyhljdwJoyjm/DIAiphgikchtK1asyBd1Yqe9GGNbxBRYLHdRYZeTk3MK53w45/xoADWLpys+LywsvF1Ms5QxBSh8u7KMqTgWDAYv4ZzfIroHIL7ovtF1/Z78/PwVpWw6Tdf1qxljpxTb/o2iKLfm5eUJPyt8VFW9FsBLuq63VxQlAOAjAGdomvZFtGK/fv3SN2zYsJ8xdivn/AgAFwOoA+A3zvkd4XBYZDqMR2DPGLsPgMC+AYBdjLEfdV0X5YwpouKpJ9HvAACCOzGttYNz/p5oL/qlHit+AoHAE4yxkUVFRS1Xrly5JtpfdnZ2W0VRljHGLguFQm+pqnouACFMRLZFZGTmAXhI0zQxhRbt++C0V1ZW1uGZmZlPATit2N51IjPDOX/ARFykqao6C8DRiqJ0y8vL+z07O7udoihiSuxjTdMuKgv4RMRPsf3DOOfPAvivpmnvmfFLnxMCiSBA4icR9KhupUegIvGTnZ1dRVGUdeLLT9O07BjxI75s7wWwRNf17bVq1Vq4e/fuWZzzdgAe5pwvEdNljLG7ALyladpVxYJA1XV9IYDVnPPRnPMtiqIMA3CSruvH5efn/1xaaAjxA0Cs/xBCZzRjrEbxr/pquq63y8/P3xwrfiKRyAxFUU4EMA3A87quv5Ofnz83Ozv7ZEVRvgLwtqIob0UiEb1YkIwA8IKmaUOK14MIm69RFOXUoqKifCFmyrBpHIAhACYoijI9Eok0YYyJqbJauq53F3WiNgHYzjl/A8BnjLEgAPFlvkDTNDGdaCZ+hDjQNU3rUSxyhLBYrGmaEAPGExU/xRj9xDkXNlXnnAvhUpcx1jwUCu1q06ZNk0gkspwxllucSdqu6/pRQngCWKlpmvh3VIAIcbtdiB/G2CLO+fnF/gqR+pAoFyt+inELFwsZ4/PiMmMAXFlYWNg0IyOjO2NMiNIXGWPTIpGImC66B0BHocs0TVtfes2Pqqr/A5DNOb+bc75BURQxjSUyMhM0TRtaEXjBYFCs+xHCepmmaX2Kp7uaFRUVdVq5cuUOh8RPkHOeJ6bNQqHQ9Wb80ueEQCIIkPhJBD2qW+kRiIqfpk2bZkTB2LZtW5XCwsJW4hc257y/yHCEw+FxUfHDGJsRCoVEJsN4AoHAlYyxVxlj54ZCoU9i/n4zY0wIhe6apv0aDAbf5pyfpet6ayFaRLnixcm/McbeC4VCj5Qjfv5ijGWLL3FRp/hXvBBYj2uadk/pBc9lTXupqipETl9N086LnTZSVfVnkSnRNE1kcMSX+iFrfmJtysnJEQJOfME9HwqFRObHeNq0adMiEonkieyMpmkXx9j0aigUujpGEIgF2DcqilI/Ly9va3kBKNYZKYqykDF2TSgUekWUKxYHdyuKkhNdWBsjfvI0TRPiUyxWF5z8lzH2TpSTYDB4qpgGSk9Pv2D58uVirYvxBIPBp4rXdhlrnKIChHN+STgcfifGbrEGa09UJJWe9lJVdUaxiGkl8C3mdT2Ad4VQCQQC9zLGHklPT28S7T8QCLRSFOUGxthLwp8yxI8Q2S/HCglVVW/inBeFw+FJZoM3GAxezTl/WWQKARyrKMqxeXl5P5VXL9HMj1h7pijKDsbY9FAodLaZffQ5IZAIAiR+EkGP6lZ6BMrZ7RXFRQiUMZqmPSG+0GLEz9OhUOi2mC9G8SXZX9f1Ws2bNz+4wHTdunWNFUUR018PaJr2sKqqGxhj8yv6YihH/BiZmViyVFUV4qdALGq1In6idUU2izEmhF22oigdhBABsF/TtJZWxE8gELieMfZiVNCVsulzMdWiaVrDmMzPlZqmvR4jNox1J0VFRS1ip4hKB2IwGJzIOb9U6JPCwsIC8XlmZmYLMZ0ldqNFMx8x4uf/NE0bFG0nJyenl67rc0qLGDH1FgwGW+i6ni2m7MSUlLBZLDSOzb5E/38MxzM451nhcFisOSqR+SkWW/0ZY1NFFk9MYQaDQTH9+b6iKB3FtFOxPT8A2CSmrgD8r1q1ajOXLFli+FYsxErs9goEAl8VZ+e+4px/KXZmxbMQvthOMVUoptuMGKxowMsSP5zzT8Ph8DmV/uVCADiKAIkfR+Glxv2OQFT8MMbEF6Dx6LouFm1uK/3lXN5C4uLpiZMqwOolTdMGq6paWLxG6OCXdOk65YifuzRNe7yU0PgGwBGapgWtiB+xfiQjI2O82A4PQGS51gghxjkXAqiKpmlZFsXPPYyxR3VdPyI/P19MCR58VFX9PwCXFa+PKrH9PlooEAiIXUFiAXPL8tb9tG3b9rCioqINxeuSyoJVrNVpJjJhUfHDOX8uHA6LKUTjyc7O7qEoys/R9TZi01IgEHiIMSZEpFgTJIStmNLKELvJov6Ut928WIhki+nPYpxKbHUvtmMtY+y7UCh0STAY/JpzXqt4x5Vhk6qqYjryVgAnAKgGYC+ADxhjNwtfSvddnEm5o3h9mdEvAJF1uyMUCn1qZWxG101xzo8Kh8PiyIByHwnix1jjVDwtd5MV+6gMIWAXARI/dpGjeoTAgS8k45yfsnZ7lQaoPPETCATEF1g/xtjpZYEqFiGLL3pVVcX01dzSmZ9AIHAM53x/fn7+wnLEzzOapol1KLFCYymAbZqmHWtF/Kiq+qXIcHDOr8zIyJi5fPlycY6RmB4S5wO1tCp+gsHgDWJdTTmZH9FHR03TmpW2KWq4FfGjqqoQh5M559enpaWV2PIfiUSOZoyJ9Tw3a5o23qr4CQQChmgT9XRdfz867RgMBsXi83sTFT/F4mYUY0wIsPac83zG2KDolF0sdyL7lp6e3jMSiQxkjAk8DeFW0Tk/xdOK/+Gc384YE1OMR6xYsUKcr1Ph46b4CQQCQ8W5WJzzC8Lh8IdmttHnhEAiCJD4SQQ9qlvpEZAkfoypIMZYp1AoJKajjEdV1e5ikbKiKE/l5eV9HQgExBkqYuFxq+h6l+K1IRrnfF44HB5YjvjJb9q0aZuZM2cWiXZzcnI66LoufsXfp2na6NJCo3Xr1kekpaWtiT3nR1XVPZzzaeFwWEwlGU/x9mSxUHe7pmlHir8Fg8H7OOdieuTgOT+xNgWDQbGoNbf0mp9WrVodmZ6eHuKcfyj6SET8BAKB+Yyx+sVTcSW2tXft2jVj165dYi2NEH5t+vXrlyZ2e5llforX5KhRkVcMQVogEPiFMdY1Og1nN/NTzIs4X0nsdvtOiMOqVas2jU5rqao6GsCFNWvWzFmwYMH+mBgR649+FmuxYvuuUqVKdfF3XdefDofDz0fLx4hPsQNRLGj2hPjJycmpVxyT+9PT03OWL18uspz0EAKOIUDixzFoqeHKgIAM8ZOVlVU1MzNTLCRtVCx2lomzThhjQkSIL4EuYjFtmzZt2kciEXEAXZgx9hiAnZxzMQ1zgjg4roLMD+eciwW1zzPG6hXv+CkqFlu7SguN4vOJxI4esQbnSbGVWlVVMU0mzsoRC5/FwmSx3kVsoRfTXUL8iHaFYBP2iC9bMW3xnaZpeaUFWTAYfJFzfl10t5eu62Jr//0A6kUikW5iC75d8VN8SJ84L2ZUKBQSO+oOeVRVfQbAcLEjrXHjxt9aFD9iF5awcbSu6zPS0tIacc6Fj2LXGeOctxXb3RMRP8X4iW34pzHGJoZCoRuixmdnZx+nKIo4zkCsHXqBMfZP8XTWYMbYwFAoNKWMBc+CM5GtE4J0saIoR4rsFedc7D4Uu9NMD0J0IvMTc8ghFEWpwRgTmS6x+6yhruv/EbsLK8O7g3xMLgIkfpKLP/We4gjIED8CglatWtVOS0t7UFGU8znnTcQZOmJX2P79+x+MXTtUfF2DOHju2OJdV7+KKw3C4bA4T0iIj0PO+RHnBXHOC4uvFhBZg8/2799/x6pVq/4szjgcsr4mEAg8zhi7kTGWtn//fnG2kJ6Wlja2+HyhqmLND+d8qqIo28TZLGlpaR1yc3OXimxQJBKZxjnvJhblapp2Rjnn/AzlnA8Wy2vEUQCMsf/pui4Ox1tZnk3i72bTXqqqil1MQhDklLe4N3p+DoAvmjZteo4V8VO80FtgItY8CaG3SWw9j0Qi74mFxJzzG8Lh8MRExU8gEBC2T9J1vasQs7HDIxAInFl8/IE456cqY2x5cWbnXVGudN8dOnSos2/fvkcAiKtORExtZ4x9kZaWdnfsjrWKhqAD4qes6y3E2i+B5RPRs6dS/LVA5qcAAiR+UoAkMpEQsItA8Tk/h+z2stse1XMWgUAg8AljrJE4m8jZnqh1QqByI0Dip3LzT977HAESP94nuGnTptVr1KgxnDEmtsFfxhg7x+puLO97RxYSAt5EgMSPN3khqwgBKQiQ+JECo9ONMFVVxenTh3HOxQLlg/dpOd0xtU8IVFYESPxUVubJb0KAECAECAFCoJIiQOKnkhJPbhMChAAhQAgQApUVARI/lZV58psQIAQIAUKAEKikCJD4qaTEk9uEACFACBAChEBlRYDETxnM67rOt24tAOclDodN6RhhjKFevRrwm1+CFPIt9UKTOCPOvISAX+PRr35F3/sNGtS0rWFsV/RS4Mq2RRyHu3Xrbui6f8SPogjxcxj85pfgnnyTPQKcb484cx5j2T0QZ7IRdb49v3NWvz6JH6lRROJHKpyON+b3Ae5H0UqcOT4spHdAnEmH1PEG/c4ZiR/JIUTiRzKgDjfn9wFO4sfhAJLcvF/j0a9++Tl77HfOSPxIfnmR+JEMqMPN+X2Ak/hxOIAkN+/XePSrXyR+JA8Al5oT8UjiRzLYJH4kA+pwc/RSdhhgB5onzhwA1eEmiTOHAXageb9zRuJHctCQ+JEMqMPN+X2AU+bH4QCS3Lxf49GvflHmR/IAcKk5yvw4ADSJHwdAdbBJeik7CK5DTRNnDgHrYLPEmYPgOtS03zmjzI/kwCHxIxlQh5vz+wCnzI/DASS5eb/Go1/9osyP5AHgUnOU+XEAaBI/DoDqYJP0UnYQXIeaJs4cAtbBZokzB8F1qGm/c0aZH8mBQ+JHMqAON+f3AU6ZH4cDSHLzfo1Hv/pFmR/JA8Cl5ijz4wDQJH7kgrp3714UFu5D7dqHmza8adNGNG7cxLRcbAF6KccFlycKE2eeoCEuI4izuODyRGG/c0aZH8lhRuKnfEBHjBiKU045DSeffFqFqF966UDcdttd6NTpKFxzzWW46aZb0KVLtwrr/PjjbHzwwTsYN26iUe4//+mLN9+cgsaNG1dYz+8DnDI/kge4w835NR796hdlfswHhLjncsPWPWhWv4Z5YZdKUObHAaBJ/MgF9YILzsLddz9gKn6++GI6xH/jx0+OywB6KccFlycKE2eeoCEuI4izuODyRGFZnN08djYK/ilCp9b1cMuATp7xjTI/kqlIZfGzceMGXHfdVTjllNPxySfTUKdOHQwdOgI1alTH+PHPokqVali9eiX+7//eRCQSwdNPP4a8vFxjqunWW28zMjXiEX8bM+YJrFq1Ak2bNseIEXegY8fOGDJkME4//SzjPyFqxP9+8smHKCoqwsCBF+OKK64x6kcFz+eff4IZM75CRkYm7rnnAfTq1Rdjxz6FhQvnY+vWrWjVqrUhjBRFwdVXX2K007Jla7z++rvo06cbpkz5FE2aNIXICr300gSIaTHx+bBhI5GT0xbC3xtvvBb9+5+Pd955F9WqVcPgwTca/vvhkfXy8hoWfvWLsgheizRr9vg1HmX5dfXj3x0E8pU7T7AGqsOlKPPjAMBWxY+49X3XnkIHLCjZZM3qmcbN5VYeIQYGDDgbZ5xxNoYPvwO//PIzHnnkPtx553144IG78eijT+Doo49BlSpVccUVF+G0087ERRddaoiRhx++D2+9NcUQEAMHnoNLL70S5513AWbO/Bbjxo3BtGmfY9iwG0uIn1q1auOZZ8Zh586dGDr0Otx2293o0+e4g+JHTHXFZn5efnkSNC0PDz30GBhjePzxR6DrOh56aLSR9YnN/ETFT0FBAa6//iqMGvUUunY9Gl9//QUmTHgO7747DeIz4e+1116Lyy+/Fl9//RWeffYpTJ8+A1WqVLECmafLyHp5ec1Jv/pF4sdrkWbNHr/Goyy/SPxYi6OUL2VF/Ajh88Ar87B+S4Hj/op51oeu7m5JAEXFzxdffAshTMQjMiNnnnk2nn76cXz//U/gHPj998W4//678NFHXxy0/667RuCYY3qhefMj8NhjD+PDDz87+NnSpb8jJ6fNIeLn5puH47jjjjfKvfTSi0Zm5r77Hi5X/OzY8TcYU1C9enVs2LAeU6a8Z2Sinn9+UrniZ/r0j42yDz446qA9Irt1/vkDjGyUED8///wzOM9EYeF+9OvXA1Onfma6Vshx4iR0IOvlJcEUqU341S8SP1LDxLXG/BqPsvwi8eNaKCa3I8+JnwY18NBV1sXPVVddgq+++v4giCLjEwgE8OmnH2Hq1OkQwu3bb2cYmR6R5Yk+YhpMTF1lZbXE1KnvY9KkVw8hovS012OPPYNAQDXKffzxh5g9+3uMGTO+XPGzbt1aPPnkKOTnh9GyZStkZmZi//79xjqf8jI/b775qiHkrr9+SIxPdyE7O4iTTjrZED+hUAhbt+42fIudLktuJCXeu6yXV+KWyG3Br36R+JEbJ2615td4lOUXiR+3IjHJ/VgRP8JEr057XXjhuZgxYzaqVq1qIHnDDVfj3HP745VXJhtraITdixYtNNb7iGmu6COyNjVr1oSmhfDoow+UyPyIrI7ItAghFbvmZ+TIu9CjRy+jiUmTXsDWrVuMNTyxU12x/7711pvQtm17XHPNdcY6n/fffxs//DCrQvEjprlWr15VIvMzaNAVOOec841pMBI/SR4wNrqX9VK20bXjVfzqm1/9IsFqPiRI/Jhj5IsSVsWPF52NTnuJdTwiUzJnzg/GFNZdd91nrJOJih+Rbbn00gG45JIrjPVBK1euwC233ICHHhqFTp264L//Pd9Y83P22ecdXPMjskZCvMSKH7FQWmR/hOgZOvR63H//I+jWrXsJ8XPxxf1xww03o2/ffhg06HIce+zxuOyyq7Bq1Urceedw1K1bFy+++Aq++eZrvPPOG3jllbcNaKMZHGHrNddcikcfffLgmp/nnnsG7777IQoLC0n8eDEQTWyiL9LUI404q7yckfhJPe5tWewH8XPhhZfgyy8/Q/369Y2FzwA3RFBU/Ahg/vhjtbGjKxTKQ40aNXDxxZejf/+BBmbhsIYxYx43RFHz5kdi5Mg70aZNu0N2e3Xv3gNz5/5kLFoWO73EAmnxxGZ7Xn/9ZYipK7E+SEypPfHEo9i8eTMaNWqME0/8D6ZNm4KPP/4S27dvM9oXYkesN4qdvhIibvLkF4y1Py1atMTQocON9T5RsUfTXrZCPWmV6Is0adDb7pg4sw1d0irK4ozET9IodLdjP4ifH3+cXwI0WYMgtlGr5/c4zZ4Tvjlts9X2/eqbX/2iKRSrke2tcn6NR1l+kfjxVrw6Zg2JH2vQkvixhlMipWS9vBKxwYm6fvWLxI8T0eJ8m36NR1l+kfhxPgY90QOJH2s0kPixhlMipWS9vBKxwYm6fvWLxI8T0eJ8m36NR1l+kfhxPgY90UMqi5/yAJQ1CDxBUCkjyDcvslKxTcQZceYlBPwaj7L8IvHjpWh10BYSPw6C60DTsga4A6Yl3KRfffOrX5T5STjkk9KAX+NRll8kfpISlu53SuLHfcwT6VHWAE/EBqfq+tU3v/pF4sepkeBsu36NR1l+kfhxNv480zqJH89QYckQWQPcUmcuF/Krb371i8SPywNEUnd+jUdZfpH4kRRoXm+GxI/XGSppn6wB7kWv/eqbX/0i8ePFUWRuk1/jUZZfJH7MY8gXJUj8pBaNsga4F732q29+9YvEjxdHkblNfo1HWX6R+DGPIV+UIPGTWjTKGuBe9NqvvvnVLxI/XhxF5jb5NR5l+UXixzyGfFGCxE9q0ShrgHvRa7/65le/SPx4cRSZ2+TXeJTlF4kf8xjyRQkSP6lFo6wB7kWv/eqbX/0i8ePFUWRuk1/jUZZfJH7MY8gXJUj8pBaNsga4F732q29+9YvEjxdHkblNfo1HWX6R+DGPIV+UIPGTWjTKGuBe9NqvvvnVLxI/XhxF5jb5NR5l+UXixzyGfFGCxE9q0ShrgHvRa7/65le/SPx4cRSZ2+TXeJTlF4kf8xjyRQkSP6lFo6wB7kWv/eqbX/0i8ePFUWRuk1/jUZZfJH7MY8gXJUj8pBaNsga4F732q29+9YvEjxdHkblNfo1HWX6R+DGPIV+UIPGTWjTKGuBe9NqvvvnVLxI/XhxF5jb5NR5l+UXixzyGHC8RCASOYYxNZIypABYrinJFbm5uOLbjYDBYk3P+N4C9MX+/X9O0MVYMJPFjBSXvlJE1wL3j0b+W+NU3v/pF4seLo8jcJr/Goyy/SPyYx5CjJbKysqpmZmau5JyPzMjImFpUVHQngFM0TetdSvz05pxP1jStnR2DSPzYQS15dWQN8OR5UH7PfvXNr36R+PHiKDK3ya/xKMsvEj/mMeRoCVVVTwPwlKZp7Ys7SlNVdQvnvFc4HM6Ndq6q6o0A+miadrEdg0j82EEteXVkDfDkeUDix4vY27XJr/HoV79IsJpHukzxwzkHY8y8U5MSIh7r169puyHbFRO23EYDqqreyhjrHQqFLohWDwQC8wGMDofD02LEzyQARwGoDeAwAO+lp6fftXz58kIr3Qrxs317AXSdWymeEmVEoNSpUwN+8yv64iLfUiIMDxpJ8ZhafNE4Sz2+ZHJ25ehvDwLw2t0n2gYjf/0OjJuyGGf3aYmTuh1hu52ob3XrHmZbw9iumJDVNisHAoF7xVofTdMujxE6sxljk0Oh0Fsxf3uGc74/Eok8JgRQenr6hwC+0DTtAStdC/FjpRyVIQQIAUKAECAE/I7AWSM+Oeji9GfOse3ulG81vPFFLtq3rofHbuxju51oRZZACimlxI+qqsM55z3D4fCAqPMi88MYe1TTtI/LQzIQCPRnjN2jaVoXK2hT5scKSt4pQ1kE73Bh1RLizCpS3ilHnHmHC6uWyOJMVubns59WY+rMFWjeoAYeHdTDqhtllhO+VZrMj6qqpwN4TNO0TsVoiDU/WwH00DQtL4pQMBh8RNf1V8Ph8Erxt0AgcLGiKENCoVAvK2jTmh8rKHmnDK1F8A4XVi0hzqwi5Z1yxJl3uLBqiSzOZK35+fzn1fhw1krUPiwTzw5JLPNTqdb8NG/evFr16tVXAbg9PT39PbHbizF2TigU6hobDMFg8FPO+Z7du3dfXbt27QaRSGQ6Y+zFUCj0opWgIfFjBSXvlJE1wL3j0b+W+NU3v/olmPOrb371izgzf/PJFj/paQyTRvZLaOFzpRI/gqKcnJyuuq5PFP8EsEjX9Svz8/NXqKq6jDE2OhQKvd2yZctGGRkZEwAcD6CIcz4xHA6L9T6W1vKQ+DEfDF4qQS9lL7FhzRbizBpOXipFnHmJDWu2yODBQjYAACAASURBVOJMtvgR1k8YfiyqZqZbc6SMUpVO/NhGKo6KJH7iAMsDRWUNcA+4cogJfvXNr35RFsGLo8jcJr/Goyy/nBA/T97QE/VrVzMnp5wSJH5sQ1d+RRI/DoDqYJOyBriDJtpu2q+++dUvEj+2Qz2pFf0aj7L8ckL83H9lN2Q1rmWbdxI/tqEj8eMAdElpUtYAT4rxJp361Te/+kXix4ujyNwmv8ajLL+cED/DL+yE9i3rmZNDmR/bGMVdkTI/cUOW1AqyBnhSnahggNerdxi2bt3tu0M3/egXiR8vjiJzm/z6DpHllxPiZ/DZbdGjbWNzckj82MYo7ookfuKGLKkVZA3wpDpB4seL8Nuyya/x6Fe/SLCah7kT4ueS/6g4sWtz885J/NjGKO6KJH7ihiypFeilnFT4bXVOnNmCLamViLOkwm+rc1mcOSF+zunTEuI/uw+t+bGLXAX1SPw4AKqDTcoa4A6aaLtpv/rmV78oi2A71JNa0a/xKMsvJ8SPyPqI7I/dh8SPXeRI/DiAXHKalDXAk2N9xb361Te/+kXix4ujyNwmv8ajLL+cED892jbC4LPbmZNTTgkSP7ahK78iZX4cANXBJmUNcAdNtN20X33zq18kfmyHelIr+jUeZfnlhPhp17IuRlzY2TbvJH5sQ0fixwHoktKkrAGeFONNOvWrb371i8SPF0eRuU1+jUdZfjkhflo0rokHrjzanBzK/NjGKO6KlPmJG7KkVpA1wJPqRAUD3I9bwokzL0ZbxTYRZ5WXMyfET/3aVfHkDZbuGi8TeMr8OBCPJH4cANXBJuml7CC4DjVNnDkErIPNEmcOgutQ07I4c0L8VM1Mw4Thx9n2nMSPbeho2ssB6JLSpKwBnhTjadrLV4c30rSXF0eRuU1+fYfI8ssJ8SNYmXxbP6SnKeYElVGCxI8t2CquRJkfB0B1sElZA9xBE2037Vff/OoXiR/boZ7Uin6NR1l+OSV+nh3SG7UPq2KLexI/tmAj8eMAbElrUtYAT5oDFXTsV9/86heJHy+OInOb/BqPsvxySvw8ck13NGtwmDlBlPmxhVHclSjzEzdkSa0ga4An1YlyOverb371i8SPF0eRuU1+jUdZfjklfu64+CgEj6xjThCJH1sYxV2JxE/ckCW1gqwBnlQnSPx4EX5bNvk1Hv3qFwlW8zB3SvzcdF57dA02NDeAxI8tjOKuROInbsiSWoFeykmF31bnxJkt2JJaiThLKvy2OpfFmVPi54pTgziuczPbvtWvX5PZqgzAdkW7HaZCPRI/qcDSvzbKGuBe9NqvvvnVL8oieHEUmdvk13iU5ZdT4qf/ca1wRs8sc4JKlSiK6Hj/u3zcekk32xrGdsW4rU2hCiR+UogsALIGuBe99qtvfvWLxI8XR5G5TX6NR1l+OSV+Tu1+JAaekG1OUKkSy1ZvwzPvLcJnY861rWFsV4zb2hSqQOInhcgi8ZNaZBVbK+ul7EXn/eqbX/0iwWo+ipwSP306NMHVZ7QxN6BUicX5W/Dc1CUkfuJGzqQCiR/ZiDrbHr2UncXXidaJMydQdbZN4sxZfJ1oXRZnTomfztn1MfSCjnG7TuInbsisVSDxYw0nr5SSNcC94k+sHX71za9+URbBi6PI3Ca/xqMsv5wSP9nNauPuy7qaE0SZn7gxslWBxI8t2JJWSdYAT5oDFXTsV9/86heJHy+OInOb/BqPsvxySvw0rlsdowf3MCeIxE/cGNmqQOLHFmxJqyRrgCfNARI/XoTetk1+jUe/+kWC1TzUZYsfxgDOgcOqZWDcLX3NDSDxEzdGtiqQ+LEFW9Iq0Us5adDb7pg4sw1d0ioSZ0mD3nbHsjiTLX6E6Nm9dz+ECHrp9uOhiH/E8dCanzjAiqcoiZ940Ep+WVkDPPmeHGqBX33zq1+URfDiKDK3ya/xKMsv2eJHTHdt2rbHIOb5YX1Ro2qGOUkxJUj8xAWX9cIkfqxj5YWSsga4F3wpbYNfffOrXyR+vDiKzG3yazzK8ku2+BELnfPX7zCIeey6HmhUp7o5SSR+4sLIVmESP7ZgS1olWQM8aQ5U0LFfffOrXyR+vDiKzG3yazzK8ku2+Gnfsi5y/9iOiM5xz2Vd0bpZbXOSSPzEhZGtwiR+bMGWtEqyBnjSHCDx40Xobdvk13j0q18kWM1DXbr4aVUXa//cjR0Fhbjlgo7olF3f3AgSP3FhZKswiR9bsCWtEr2Ukwa97Y6JM9vQJa0icZY06G13LIszJ8TP9p37sH5LAa45ow16d2gSl4+05icuuKwXJvFjHSsvlJQ1wL3gS2kb/OqbX/2iLIIXR5G5TX6NR1l+OSF+Cvfr0Nb+jYtOyMbJ3Y80J4kyP3FhZKswiR9bsCWtkqwBnjQHKujYr7751S8SP9ZG0b7CCKpkplkrXEGpvfuKUK1KesLt+DUeZfnlhPjJTE/DQm0zzuzVAucf2zouDinzExdc1guT+LGOlRdKyhrgXvCFMj9eZCE+m/waj7L8+nDWCnz1yxoMv7Az2rSoEx+4MaV/WLIBr36Rh0v+o+LErs1tt0OC1Rw6J8RP3ZpVMHvxRvQ7qhkuPyVobgRlfuLCyFZhEj+2YEtaJVkv5aQ5QJkfL0Jv2ya/xqMsvx55/Ves2rgLA4/PxqnHxDfdESWFc477Xp6HDVsK0LNdYww6q61tvkj8mEPnhPg5ouFh+HLuGnTLaYgbz21vbgSJn7gwslWYxI8t2JJWSdZLOWkOkPjxIvS2bfJrPMry67YJc7B1576ExM+qjTvxyOvzDY5I/JQfqrI4c0L8iKzflO9XIOfIw3H7xV3iGm807RUXXNYLk/ixjpUXSsoa4F7wpbQNfvXNr35RFqHiUSQyNtc9PQtFET0h8fPWjBC+W7iexI/JS0vWOHNC/Byd09CYtmze4DA8fE33uF6/JH7igst6YRI/1rHyQklZA9wLvpD48SIL8dnk13iU4deef4owZOxsA1C70177i3QMH/8jCv4pIvGTwuLn+KOa4fkPf0edmlXwzE294xpkJH7igst6YRI/1rHyQkkZL2Uv+FGWDX71za9+Uean4pEk7nO6e/LchMTP/Ly/MOHjpQc7ommv8jGXNc6cyPyc1SsLj721EBnpCiaN7BfXK7hSip9AIHAMY2wiY0wFsFhRlCtyc3PD5SGnquqbACKapl1pFV0SP1aR8kY5WQPcG96UtMKvvvnVLxI/FY8ica7L428vTEj8jJ2yGEtWbCXxY+GFJWucOSF+/ntiAPe89IvhxYsjjkOVDOtHH1Q68ZOVlVU1MzNzJed8ZEZGxtSioqI7AZyiaVqZObNgMHgO53wagDdJ/DDUq3cYtm7dDV3nFoZN6hSRNcC96LFfffOrXyR+Kh5FsVkbO9NeO3bvw4gXfoLOubFWZN3m3bTguQLIZY0zJ8TPtWe2xbBxPxrWP31jL9StVdXyK7jSiR9VVU8D8JSmadF9cWmqqm7hnPcKh8O5scipqiouC5kD4AcA6SR+SPxYHlkeKijr5eUhlwxT/OqXn32Twdl3C9fhrRma7cyPOB/og+/zUbdWFXRRG+Cb+etI/KSo+BF3eg16cqZh/QNXHo0WjWtafk1VRvFzK2OsdygUuiCKUiAQEPsdR4fDYZHhOfgEAoEPFEX5mnN+BIAst8XPxq0F2FlQiOCR9g/xshwJFgrKeHFZ6CYpRci3pMCeUKfEWULwJaWyDM4+/mElPp2z2pb4ETvF7n9lHtZvLsCZvbJQuD+CGb+uJfGTouJn+MDOGPLsbOzZV4QRF3VGu6y6luO60omfQCBwr1jro2na5VGUVFWdzRibHAqF3or524Wc86vC4fCpqqo+aEf8bN9ekND00PDnf8T2Xfvw6KBj0KzBYZZJdaqgeHHVqVMDifrllH2JtEu+JYJecuoSZ8nBPZFeZXD2+pd5+P63A1vULzwhG6f1aGHZpNUbd+LBV381yj9xfU+ILNLX89aiV/vGGHx2O8vtlFVQhm8JGeBQZVl+XTn624MWvnb3ibat/eyn1Zg6cwU6tKpnCJ47XvwJf27fixvObY9j2jay3O6i/C0Y+8FifDbmXGa5UqmCtiva7TCReqqqDuec9wyHwwOi7YjMD2PsUU3TPhZ/a9myZaOMjIyfIpFIvxUrVqy1K34SsVPUPe/26cZZFted1wFn9mmVaHNUnxAgBAiBlEdg9Gvz8PPvGw0/rjqzHc4/PtuyT5M+WoLPflyFNll18eTNffF/nyzFJ7NX4PiuzTH84q6W26GC8SNw1ohPDlaa/sw58TdQXGPKtxre+CIXXXIa4qFBPTHyudkIrdmO68/viDN6t7Tc7q/LN+Hhl3+pVOLndACPaZrWqRglseZHLPvvoWlanvhbMBi8FMAkzvn+4jJiFZUCYIamaWdaQVfs9ko0Q3LtE9+hKMKNlOx15yT2q8SKzWZlZP0CMOsnGZ+Tb8lAPbE+ibPE8EtGbRmcPfrGfOSv22GYH0/mR5ztM+z5H1CwtwhXnZ6D4zo3w7vfaJT5MQkEGZyJLpzK/Ix5f5Gxc++8Y1vhnD7WxU+ly/w0b968WvXq1VcBuD09Pf09sduLMXZOKBQqV/bbzfwkuitq8FPfG+Kn4eHV8Pj1PZPxrirRp4z5+qQ7UY4B5JtXmSnfLuKscnJ258Sf8dffew3n49nttSD0F174aCky0xWMGdIH1aum471vw7Tmx4L4kbHL14ndXmLNz0vTl+PnZZtwUrfmuPgkcXqNtafSrfkRsOTk5HTVdX2i+CeARbquX5mfn79CVdVljLHRoVDo7Vj4ki1+hC1jb+6DWjUyrbHqUCn6snEIWIeb9StvfvVLhINffZPh1w1jZmFfYSRu8TNu6hKIX/s92jXC4LMOZNJJ/Ji/fGRwJnpxSvy8+00Y/5svFq03wqBiXs29Aiql+LECTKJlZBxyGM38CFuG9u+IzgGx8z55j6xBkDwPKIvgp/OZKB69OJIqtilRzvbtj+CGZ2Yd7MRq5mdHQSFGjJ9jnO0z4sLOaNfywK4gEj/mMZQoZ9EenBI/0+eswkc/rEL7VnUhMkFWHxI/VpGKs5xs8XNGzxbof1zrOK2QW1zWIJBrlZzWyDc5OLrZCnHmJtpy+kqUsy1/78XtE3+OW/zMmLcG732Xb9wB9dQNvYzMGokfa5wmypnT4kfs/Hvz6xBaNqmJ+6442ppT4mqH/C14buqSyrPg2TIyCRaULX5yjjwct1/cJUGrEqsuaxAkZoUztck3Z3B1slXizEl0nWk7Uc5WbNiBUW8siEv8iLN9HnhlHtZtLkDpH5GU+THnOVHOnBY/v+b9hRc/XooGh1fFE9f3MneouASJH8tQxVdQtvgRd5a8cOuxB3+xxGeNnNKyBoEca+S2Qr7JxdON1ogzN1CW20einP0W3mzc4h19rEx7/bFpFx567cDZPqMH90DjutUP1ifxY85vopw5LX5yV2/DU+8tQrUq6cZ3pNWHxI9VpOIsJ1v8iO4furo7jmiYvMMOZQ2COKF0pTj55grMUjshzqTC6UpjiXI2a9F6vP5VKC7x8843mnGFRetmtXDPZd1K+Enix5z2RDlzWvys+XPXwYMrX7q9H9IUcSqN+UPixxwjWyWcED+XnxJEv6Oa2bJHRiVZg0CGLbLbIN9kI+p8e8SZ8xjL7iFRzqb/tBofzV5pWfyIQ2KHj5+D3Xv34/JTg+jXueT7k8SPOcOJcua0+Nm28x+MnPCT0U08u6JJ/Jhzb6uETPHTpF51bNy6B707NMY1Z7S1ZY+MSrIGgQxbZLdBvslG1Pn2iDPnMZbdQ6Kcvf0/Dd8uWGdZ/CzUNmP8tN+Rka7g2SG9Ub1qRgmXSPyYM5woZ06LH3E/2/XFOwAfvfYYNK1fw9ypVF/wnJOTU0/X9b5paWm/5ebm/mHJY5cKyRQ/fTo0wY+/b4QQQaMG9XDJg0O7kTUIkuZABR2Tb15kpWKbiLPKx5lY2CoWuEYfszU/z3+4BL+Ftxh3Pl1Xxt1dJH7MY0jWOHNqq7vw4PqnZ6KwSMedl3SBesTh5k6lmvjJycnpoOv6B5zz6zjnixRFWQhAXHq1jzF2RigU+s6S1y4Ukil+RLr2jeJ57nG39MVh1Ur+enHBHaMLWYPALXvj6Yd8iwctb5QlzrzBQzxWJMrZE28vRGjt35bEz849B872iegcwwd2QvtW9Q4xlcSPOXuJcuZ05ke0P3LCHGzbuQ9Dzu+ALmoDc6dSTfyoqjqDc75X1/VBaWlpAwHcn5aW1ikSiVwH4BRN05J/B0Qx7DLFz92XdsUz7y+COODr1oGdjNtsk/HIGgTJsN2sT/LNDCHvfU6ceY8TM4sS5eyel+YaSwCsZH7+9+tavPttGIcflomnb+xd5k5ZEj9mjMn70etk5ufBV+ZhzV+7ceVpOTi2U1Nzp1JQ/OxSFKVrXl6epqrqFwD+1DTtqmAw2JJzvkzTtH/3MFpy37lCMsXPPZd3xYczVyBvzd84u3cWzu2bnBveE31xOYd24i2Tb4lj6HYLxJnbiCfeX6Kc3Tx2Ngr+KYI4opCb3O0V/UI8vUcLXNCv7ANiSfyYc5ooZ25kfp569zfk/rEdA/q1xmk9Wpg7lYLiZ6uiKD2Lior+SEtL28Y5v0bTtPdUVRXHOn6maVojS167UEi2+FkU3oLPf/7DOJZdHM+ejEfWIEiG7WZ9km9mCHnvc+LMe5yYWZQIZ2Ln1uCnZhpdiKl/sYOrvDU/sdufRw06Bk3qlb0IlsSPGWOpkfmJrgU77ZgjMeD4bHOnUlD8TOOcpzHGtjHGBkYikSaKoog77MUlpas0TbvYktcuFJItfnYV7Me4D5cYBzk9P6wvFHbgeHY3n0ReXG7aaacv8s0OasmtQ5wlF387vSfC2fZd+zDihTlGt83q18D6LQXlip+oqGnVtBbuvbzk2T6xdpP4MWcxEc5iW3dy2ktcbyGuuejbsQmuOr2NuVOpJn5at27dMC0t7UUArTnnj4TD4Q9VVR0DoGMkErl4xYoV/24DsOS+c4Vki58Gtath2PM/GgbHs51PpoeyBoFMm2S1Rb7JQtK9dogz97CW1VMinEVPahY/+8SOHrHwuazMj8gQCZG0a89+XHZKEMdXcDYaiR9zZhPhzC3xM232Snz202ocFaiPm/t3NHcq1cRPOR6lAYhY8tbFQrLFT+umtXHHxJ+w+e9/cNXpOejb0dqiLpkuyxoEMm2S1Rb5JgtJ99ohztzDWlZPiXC2ZMVWjJ2yGDWrZ6B5g8OMNR5liZ/oFRjpaQqevbk3apQ624cyP/GxmQhnbomfGb+uhRCygea1cdelXS05mHKHHGZnZ3dRFOV2ADmRSOQsRVEuUhQlFAqFPrXksUuFnBA/k6cvw9xlfxqr2cWqdrcfWYPAbbut9Ee+WUHJW2WIM2/xYcWaRDib8/tGvPx5rjHlVatGZrni54Vpv2OBthnd2zTE9ee0r9AsyvyYs5YIZ26Jn5+XbsJLny2P6yy8lBI/wWDwBM755wA+AnA+57wtY2yQ2OYP4FJN0943p9KdEk6IH3GyqTjhtHmDGnj4mmPccSSmF1mDwHXDLXRIvlkAyWNFiDOPEWLBnEQ4+3LuH5gycwXatKhj9FRW5mfXnkLjOgtxts+wAZ3QsXXFx4KQ+DEnLRHO3BI/0axgreoZGDu0r7lTqTbtFQwGxQUeH4RCobGqqu7inHcKh8Mrg8Hg7ZxzIX6sTfZZgiaxQk6In1Ubd+KR1+cb2zzH33qssfjZzUfWIHDTZqt9kW9WkfJOOeLMO1xYtSQRzqJCRZzWvLOgsEzx8838tXjnmzBqG2f79DK95JLEjzlziXDmlvhZuWEnHn1jPtIUhsm39QOzsCEopTI/sYKnlPjx/Tk/Ys2PWMh307Ozsb9Ix8iLOqNtVl3zyJVYQtYgkGiStKbIN2lQutYQceYa1NI6SoSz6LT/f7odgXWbd5cpfh569Vf88ecuWN3yTOLHnNpEOHNL/Py1fQ/unDTX6G78sGNRvap5YiDVxM8azvnV4XD4m1Li5wIAz4RCIWunG5nznXAJJzI/wqjH3lqA8LodOO/YVjirV1bCdsbTgKxBEE+fbpUl39xCWl4/xJk8LN1qKRHOnn7vNyxfvR39j2tl/G/paa91f+3G/a/MM1x55NpjjLVBZg+JHzOEUuOcnz3/7MeQsT8Yzjx+fU80PLyaqWOpJn4eACDO8hkGYArn/DxFUY7gnD/GGJscCoXuM/XYpQJOiZ8PvsvHV/PWoFPrerhlQCeXvDnQTSIvLlcNtdEZ+WYDtCRXIc6STICN7hPh7P6X5xkZn6tOy8Hc5X8eIn7e/y6Mr+etRcsmNXHfFeLcW/OHxI85RolwFtu6k+f8cM4x6MmZ0Dk3znUS5zuZPSklfsT3r6qqQgDdBqBqsXP7GWPPNWnS5O6ZM2cWmTns1udOiZ8Fob/wwkdLjRNOnxvax9LcpiyfZQ0CWfbIbId8k4mmO20RZ+7gLLOXRDgT55yJtT63XNARYmtzbOZHLAkYOeEn4/NLT1ZxQpfmlswm8WMOUyKcuSV+RD/Dxv2AnXv2W1roLsqnmvgxsMzOzq4iDjpMS0tLLygoCK9bt26vOYXulnBK/MSecvrYdT3QqI5715nJGgTuMmGtN/LNGk5eKkWceYkNa7bY5UzXOQY99T04B+67ohumzlxRQvwsyt+CcVOXID2NYcyQPsaPQysPiR9zlOxyVrplJzM/oq/opbeDzmyLnu0bmzqWcuInKyurakZGRg7nvFp6enqJOx7y8vLEbjBPPE6JH+HcyAlzsG3nPlglWRYgsgaBLHtktkO+yUTTnbZ2FOwD0tNRp1o6xJejnx6/xqNdv0RGJ3rCvdjFJc77ic38TPjod8wPbUa3YAPceF4Hy6FA4sccKrucuS1+outh/3tiAP85+ghTx1JK/AQCgTMYY++Ie+0AY8d37MM1TROnPXvicVL8RC9xO75LM1x2ctA1f2UNAtcMjqMj8i0OsDxSNPpL0u0MqBvu+zUe7foVu5h50sh+xknPUfHTp2MTDB//I4oi3JgS65Rd3zJFJH7MobLLmdvi5/kPl+C38BZjI5DYEGT2pJT4UVV1Oed8GYBR6enp20s7l5ub+4eZw2597qT4mTFvDd77Lh8tGtXEA1dZW9gnw29Zg0CGLbLbIN9kI+p8e1Hxk6zrXpz00K/xaNev5au34en3Fhlnm71w67F46t3fDoqfjHTFOPxVnPr8zE3mZ/vE8kbixzyK7XLmtvh55Ytc/LhkI6wmBVJN/Pyj63q7/Pz8FeaUJbeEk+Inf/0OjH5zgXGz+wvDj0WVDHcSXrIGQXKZKbt38s2LrFRsE4mf1OPM7jibu2wTJk9fjkZ1q+OxwT1KiJ95uX9i9aZdOLX7kRh4QnZcoJD4MYfLLmdui58Pvs/HV7+ssXStibAtpcRPIBCYzxi7Q9O0b80pS24JJ8WPOOTwpmdnGWneOy4+CsEjDxz37vQjaxA4baed9sk3O6gltw6Jn+Tib6d3u+Msmu1Wm9fGnZd2PSh+endojDm/bzJMefia7saFp/E8JH7M0bLLmdvi54u5fxgL4cX1J7f99yhTxzwvfnJycnpFveCc9+Wc3wBAbHdfqShKidvcK8uCZ4GHOMpbHOk9oF9rnNbDnbMdZQ0C06hMQgHyLQmgJ9gliZ8EAUxCdbvjbMrMfHw5d83BBc3RaS+x8FMsdW/RuCYeuDL+JQAkfsyDwC5nbouf2Ys34LUv83Bkw8Pw4NXdTR3zvPhRVVUvju/SC5xLO1dpFjwLx9/5RsM389ehi9oAQ863vrvBNCIqKCBrECRig1N1yTenkHWuXRI/zmHrVMt2x9nLny83MjwndGmGS08OHsz8RO285D8qTuxq7WyfWN9I/JgzbZczt8XPQm0zxk/7HXVrVcHTN/Y2dczz4qdNmzaW0xqVZcGzYFXMc0/8ZBlq18jEmCG9XTnsUNYgMI3KJBQg35IAeoJdkvhJEMAkVLc7zsTuLnFz97l9WuLsPi1LiB9xmeWzN1s/24fET3zE2+XMbfGjrf0bj7+9EJkZCiaO6GfqpOfFT2kPgsHgCbqup4XD4f+Jz1RVfUZRlOl5eXkzTb11sYCTa36EG1t27MXtL/5sePTkDT1Rv7b5XSaJui9rECRqhxP1yTcnUHW2TRI/zuLrROt2x9lDr/2KPzbtwuWnBNHvqGYlxE9XtQFuspn9psyPOct2OXNb/KzfUoD7/u8Xo9tJI49DRnrFG4FSSvyoqno5gJcYY7eHQqHnhJPBYPBtzvkFjLFLQ6HQFHMq3SnhtPgRd5kMHz8HOwoKcf057dC9TSPHHZM1CBw31EYH5JsN0JJchcRPkgmw0b3dcTbihTkQp9uLKX4x1R+9vV2YMLR/R3QOWD/bJ9ZsEj/mJNrlzG3xI74Lb33+R6PbZ27qjTo1xUUQ5T+pJn6WM8bE7e0vx7oUCAQGA7g5HA67s/jFPF7gtPgRJoj5TTHP+Z9uR+C/JwUsWJVYEVmDIDErnKlNvjmDq5OtkvhxEl1n2rYzzsQPveuenmnsbr37sq7IblYbsVclTL6tH9LTFFsGk/gxh80OZ2W16vT1FuJ+t8FPHZgAevCqo3Fko5q+Ej97OOftw+HwylLipxVjbKmmae5ddGUSM26Iny/n/oEpM1cYN9iKm2ydfmQNAqfttNM++WYHteTWIfGTXPzt9G5nnBX8sx83j/3B6O7x63ui4eHVSoifV+48wY4pRh0SP+bQ2eEsGeJH9CmOgNm7L4LbLuqMNll1/SN+AoHA74yxSZqmjS8lfgYzxoZrmpZjTqU7JdwQP6E12/HEO78Zl/m9cKuY47T368cqIrIGgdX+3CxHvrmJtpy+SPzIwdHNVuyMs41bC3DPSwfWckwYfiyqZqYfFD/iVOexN/ex7QKJH3Po7HCWLPFzx8SfsPnvf3DDwcNKUAAAIABJREFUue1xdE5D/4gfVVWvEGt+OOdvAvhVeMYYEymPSxljN5WeDjOn1bkSboifffsjuGnMbOic457LuqJ1s9rOOQRA1iBw1EibjZNvNoFLYjUSP0kE32bXdsZZ9Ede7C6eKPckfmwSEUc1O5wlS/w88vqvWLVxFy47JYjjj2rmH/EjPAkEAhczxoYCaA9gH4A8xtgToVDo0zj4dLyoG+JHOBFd+HfRCdk4ufuRjvolaxA4aqTNxsk3m8AlsRqJnySCb7NrO+Ps17y/IC5zrl+7Kp684cCZtyR+bBJgo5odzpIlfsZ8sAhLV24zLjYVF5xW9KTUgmcbvCWtilvi580ZIXy/cL2R4hOpPicfWYPASRvttk2+2UUuefVI/CQPe7s92xln3y5YZ1xc2rppLdxTvLaRxI9dBuKvZ4ezZImfydOXYe6yP3Hy0UfgohMr3gSUcuKnVatWR6alpYlzzDPFrFcsyOFw+J34qXWmhlvi5+elm/DSZ8tRr1YVPGXhVMtEvJU1CBKxwam65JtTyDrXLokf57B1qmU742za7JX47KfV6JxdH0Mv6EiZH6fIKaddO5wlS/y88z8N3yxYh17tG+PaM9v6J/OjquogseYNQFmnF1m+3iIQCBzDGJvIGFPF5a6KolyRm5sbjkVKiKyMjAyxvqgHgN2c8wnhcHiU1bhzS/z8uX0P7po01zDLytkGVu0vq5ysQZCIDU7VJd+cQta5dkn8OIetUy3bGWevf5WHWYs24NhOTXHlaQf2tFDmxymGDm3XDmfJEj+f/rgKH/+4Ch1b18OwAZ18JX5yAczWdf22/Pz8nXboz8rKqpqZmbmScz4yIyNjalFR0Z0ATtE0rcRlIKqqzmCMLWrSpMnda9asaZqenj6Xc355OBz+xkq/bokfcQbGLeN+xO69+3HTee3RNVjxCncrtpdXRtYgSMQGp+qSb04h61y7JH6cw9aplu2Ms+c/XILfwltwZq8snH9sKxI/TpFTTrt2OEuW+Plu4Tq8NUOzdPxLSk17qaq6R1GUznl5eZpd/lVVPQ3AU5qmRRfIpKmquoVz3iscDgtxZTzZ2dlVmjdvHpk5c2ZRdnb2UYqifKkoyhl5eXkLrPTtlvgRtjw3ZTEWr9iKU485EgOPz7Zinq0ysgaBrc4drkS+OQywA82T+HEAVIebtDPORr0xHys27ETs5aWU+XGYqJjm7XCWLPETvfOyYZ1qePy6nhWClGriZxbnfFw4HP7QLvWqqt7KGOsdCoUuiLYRCATmAxgdDoenlW5XVdV5AI5mjL0aCoWuttqvED/btxdA17nVKoeUu/aJ74xTTe+7oluF29g/nbMK02athHrE4cYJqKWfiZ8sNRaBjRp0DJo1OMy2PUJVv/FVCIPPbote7ZvYbseLFcUAr1OnBhLljHxzD4ErR39rdHb1GW2MKRE/PX6NRzt+3TZhjnF2y43ntT94jU+Ue7HVfdwtfW1T/+43Gr6et9ZYIzL47Ha22xEV7fiWUIcuVZblV5QzYfZrd59o23qx/mvqzBXo0KoeRlzUuUQ7y1ZtM+59q1E1HS8MP67CPhblb8HYDxbjszHnllg7HI9htivG04koGwgErmKMPQ7gZc65yP4UxrZhZcFzIBC4V6z10TRN3BNmPKqqzmaMTQ6FQm+VtklMk6WnpzdTFGUG5/zJcDg8yYrdQvxYKVdRmfNunw5xZPfTQ/si2KL80yoXa5tx76SfkJmRhvdHnX7IUe9njfjE6KZdq3p4/Cb7B4JF2xFtTX/mnETdo/qEQEIIRONxyIDOOKVHi4TaosreReCCuz7DvsIIRt/YGx1aH7jDK8r94TWr4M0HT7Vt/P99shSfzF6B47s2x/CLD/3haLthqngIArK+P6Z8q+GNL3LRJachHhpUMruzYt3fGPbsLDAGfPTk2UhTypcnvy7fhIdf/iU1xI+qqnoFMWVpwbOqqsM55z3D4fCAaFsi88MYe1TTtI/La19V1REA+mmadpaVuHYz87N3XxFufGYWhNoSd5pkNalVwsSo4m7ZpBYeuEpslLP3yFLu9np3tpasXzfOWmmvdb/6Rpkfe/GQzFrxxqIQPeJeL/GMHtwDTevXMP5NmR/3WIyXs/Isk/X9UVHmZ+uOfyAuwRXP88P6omZ1sSm87CelMj8y6FZV9XQAj2maFl0KLtb8bAXQQ9O0vGgfwWBQrO25KhQKLRF/U1X1bgBtNE27zIodbq75Efbc//IvWLe5oMS8eNTO6Px4yyY1cd8V9sWPrIvprODndhlZ89pu222lP7/6Rmt+rLDvrTLxxuJff+/FnRN/PvhlVqNqhvFvWvPjHq/xclaeZbK+Pz7/eTU+nLUS7VvVxfCBJae9hFi+YcwswwSxzKNJvQNiuawnpdb8yKC7efPm1apXr74KwO3p6envid1ejLFzQqFQiZynqqqvATh89+7dF1evXj1LTHvpun51fn7+DCt2uC1+XvsyD7MXb0CPdo0w+KySc9ckfswZkzXAzXtyv4RffSPx434sJdpjvLGYv34HRr+5wLi/cNLIfuI6IxI/iZIQZ/14OUum+BGrTa57epaxXOSuS7sg0Pzw1BU/qqpOtsqVpmmDrZTNycnpquv6RADi0IhFuq5fmZ+fv0JV1WWMsdGhUOjtrKysw6tUqfIC51xMKG/nnI8Kh8OvWmlflHFb/PyweANe/TLPuPFY3Hwc+5D4MWdN1gA378n9En71jcSP+7GUaI/xxuJCbTPGT/sddWpWMc4xiz6U+UmUCev14+UsmeJH9C2mvbbv2oeb+3fAUYEGqSt+AoHA91ZoYoyJNT8nWCnrRhm3xc+GLQW49/8O3Hw8dmgf1IqZ6yTxY864rAFu3pP7JfzqG4kf92Mp0R7jjcWZi9YbO0xbNKpZYr0iiZ9EmbBeP17Oki1+7n95HtZt3o2rTs9B347l7wKtdNNe1ilPrKTb4kfc7H7z2B8gFj8P7d8RnQMHdkWIh8SPOZeyBrh5T+6X8KtvJH7cj6VEe4w3FsUxHh//sMrY1nzrwH9P7CXxkygT1uvHy1myxc+T7yxE3pq/jTPvxNl35T0kfqzHQFwl3RY/wrhn3l8Ecc7BGT1boP9xrUn8xMGYrAEeR5euFfWrbyR+XAshaR3FG4tvzQjhu4Xr0btDY1xzxr93NZH4kUaJaUPxcpZs8TPho98xP7QZp/dogQv6/fs9WNouEj+m1NsrkAzx8/EPK/HpnNVo06IObvvvUSR+4qBO1gCPo0vXivrVNxI/roWQtI7ijcXoF9lpPY7EgH7/nl5P4kcaJaYNxctZssXPG1/lYWapu+DKsonEjyn19gokQ/z8vnIrnv1gMapkpuGFYccaJ46Kh6a9zDmUNcDNe3K/hF99I/Hjfiwl2mO8sfj4WwugrduBi07Ixsnd/53CIPGTKBPW68fLWbLFz4ezVuDzn/9AF7UBhpzfoVxHSfxYj4G4SiZD/BT8s99Y9yOeh67ujiMaHrjKgsSPOXWyBrh5T+6X8KtvJH7cj6VEe4w3Fu+ePBebtu3BoLPaome7xge7J/GTKBPW68fLWbLFz9fz1uD97/KN657uvKQLiR/rVMspmQzxIyy/56W52Lh1Dy4/NYh+nZuR+LFIp6wBbrE7V4v51TcSP66GkZTO4o3FIc/Oxp59RcYdTu2y/r3ih8SPFDosNRIvZ8kWP3N+34iXP89Fs/o18Mi1x/hD/HTs2LHG3r17hzHGejDGMjnnJS7u0DTtZEtsulAoWeLn5c+XY87vm0osEKTMjznhsga4eU/ul/CrbyR+3I+lRHuMJxb3F+kHr7Z4+OruaF6cyY7NZouLTcfebP++wve+DWPGr2uNrJLILiXyxONbIv24XVeWX26c8CywiU5n1a6RiWcriI2UmvZSVfVNAP0BfAVgR+kg0DTtKrcDo7z+kiV+Zv62Hm98HUKTetUxalAPyvxYDAhZA9xid64W86tvJH5cDSMpncUTi9t2/oORE34y+hUCRwid6EOZHyl0WGokHs4qatAt8bNi/Q6MenOBcanp5Nv+PRW8tG2pJn7+ZIzdFAqFplpiLYmFkiV+1v61Gw+8Ms/wXFzsJu7CocyPeSDIGuDmPblfwq++kfhxP5YS7TGeWFy1cSceeX2+cUP3S7cdf3ADB2V+EmUhvvrxcOYF8fPntj24a/Jcw5QXbj0W1aqkl2lWqomfLWlpaT1zc3PD8dHnfulkiR9d57jp2dnYtz+C4QM7oX2reiR+LNAva4Bb6Mr1In71jcSP66GUcIfxxOKSFVswdsoS1KqegbFD+5bomzI/CVNhuYF4OPOC+Nm9dz+GPndg48+T1/dE/cOrpb74CQaDz3HOFU3Thorrsyyzl4SCyRI/BuHFJ1ye3TsL5/ZtReLHAv+yBriFrlwv4lffSPy4HkoJdxhPLP6wZANe/SIPzRvUwMPXlFy4SuInYSosNxAPZ14QP+K2g0FPfg/Ogfuu6IaWTWqlvvhRVfX/AFwKYAtjLJ9zXhjrFS14PoBG9JyD9i3rYviFnUn8WBjmsga4ha5cL+JX30j8uB5KCXcYTyx+/vNqfDhrJdpm1cHIi/49tFUYQeInYSosNxAPZ14QP8IGkfkRGaDo7EdZdqXatFeFt6rTgucDFC8Kb8G4D5egepV0jBvWF9c+ceBu2JZNauK+K462HPSlC8pasGbbAAcryhrgDppou2m/+kbix3ZIJK1iPLH47jdh/G/+WvRo1wiDz2pXwmYSP+5RGA9nXhE/0fOhBp/VFj1izoeKtS+lxI97dCfeUzKnvXYWFGLY8z8aTjx67TEHb3sn8VM+r7IGeOKRI78Fv/pG4kd+rDjdYjyxOOnTZfhl+Z84+egjcNGJARI/TpNTTvvxcOYV8TP6zQXIX78DF58UwEndjijTLM+Ln0AgcHFGRsbU5cuXF4p/VwAuD4fD7yYpPg7pNpniRxhz58Sf8dffe3HV6TnGvDllfiqODFkD3CvxF2uHX30j8ePFaJM3zp569zfk/rHduJxSXFIZ+1Dmxz3uZb0/ZM0cRKdD27eqi+EDO5cJxLipS7Aofwui617LKuR58aOqqh6JRBqvWLHiL/HvisSPpmlp7oVExT0lW/xMnr4Mc5f9ieM6N8WsRRtI/JgEhqwB7pX4I/HjRSas2+TXeIzHr/te/gXrNxfg6tPboE/HJiR+rIeP1JLxcOaVzE/0sN8TuzTHJSerqZn5kcqii40lW/x8u2Ad3v6fZuyUWLe5gMQPiR9s3bob4igEvzyU+Uk9JuP5Ir1l3A/YtWc/hg3ohI6t65H4SRLd8XDmFfHz/ndhfD1vLY5p2wjXnV1yvVjURs9nfpLEd8LdJlv8rN60Ew+/Nh/i/o/o1x2t+Smf1rw/tqNajSpo2bCGrwSC8FjWyyvhQSG5ARI/kgF1oTmrsRjRdQx+cqbx7nrgyqPRonFNEj8u8FNWF1Y5MzPPzWmv6NRYu6w6GFFqpyCJHzOmEvw82eKnKKIbhx2K+3GiD4mfskkt+Gc/bn3+R4ikiDgVu1pm2SeCJhgSSasu6+WVNAfK6ZjEj9cYMbfHaizu2L0Pt46fYzT4zE29UadmFRI/5vA6UsIqZ2aduyl+Zi1aj9e/CqFFo5p44KqydzhT5seMMZufJ1v8CLMfe2sBwuv+vQKNxE/ZZGpr/8bjby888KId0ht1Div5orUZAp6pJuvl5RmHig0h8eM1RsztsRqLsdf0iPuZ0tMUEj/m8DpSwipnZp27KX4WhP7CCx8tRb1aVfHUjb3KNI3EjxljNj/3gvj54Pt8fPXLmoMekPgpm8yZi9bjja9CJH5sxnqyqpH4SRby9vu1+kW6bNU2PPP+ItSomo7nhx17SIe028s+B/HWtMqZWbtuip/Qmu144p3fUCUzDS8OP47Ejxk5Mj/3gviJqt+oXyR+ymb4nW80fDN/HYkfmQPAhbZI/LgAsuQurH6R/rx0E176bDma1KuOUYN6kPiRzEM8zVnlzKxNN8XPus27cf/LBy74LitzKP6eUpmftm3bNi4qKnqEc96DMZbJORfreQ8+4XC47D1tZqw48LkXxM/2Xfsw4oUD8+biIfFTNtHiF6b4pSkemvZyYDA41CSJH4eAdbBZq1+kImMtMtfBIw7HHZd0IfHjICdmTVvlzKwdN8XP37v3YXjxmrExQ3rj8DKWMqSU+AkEAp8wxsQE3psA/l3MUoy6pmkPmRHg1udeED/C19smzMHWnftI/FRAvBCIQiiS+HFrdMjph8SPHBzdbMXqF2l0yv7onIa44dz2JH7cJKlUX1Y5MzPRTfEjNvwMfmqmYdLDV3dH84aHHWJeSokfVVW3cc4HhsPhb8yATvbnXhE/L368FL/m/UXip5yA2LuvyNgVF30o85PskWO9fxI/1rHySkmrX6Qvf7Ycc5ZuQnmH1NGaH/cYtcqZmUVuih9hyw1jZmFfYQS3//co5LSok/LiZwPn/MRwOJxrBnSyP/eK+Jkxbw3e+y6fxE85AbFyw048+sZ8Ej/JHjA2+ifxYwO0JFex+kU65oNFWLpyG87r2xJn9W5JmZ8k8maVMzMT3RY/t7/4E7bs+Ac3ntse3XIaprb4CQQC9wLoWFBQcOWGDRv2mIGdzM+9In5WrN+BUW8uIPFTTjD8uGQjXvniXy1NmZ9kjpr4+ibxEx9eXiht9Yv0wVfnYc2fu3HFqUEc17kZiZ8kkmeVMzMT3RY/D732K/7YtAuXnxpEvzJiKNWmvb4EcDxgHFy8kXNeGAs4LXg+NPzEIYfXPX1g7pMWPB+KT+njAEj8mL3CvPM5iR/vcGHVEqtfpMPH/4i/dxfi5v4dcFSgAYkfqwA7UM4qZ2Zduy1+ohtZ+h/XCmf0zErtzI+qqg9UBDAteC4bnWjQiftxxD05dh9ZwWu3fyfqPTdlMRav2HqwaRI/TqDsTJskfpzB1clWrXyR6pzjuqdmIqJz3HN5V7RuWpvEj5OkmLRthTMr5sn6/rByq7uwZ9Kny/DL8j9xSvcjcOEJgdQWP1YA9koZr0x7CTyiv6IuOyWI4486NIVsFTNZwWu1PzfK3THxJ2z++x8SP26ALbkPEj+SAXWhOStfpLv37sfQ534wrHni+p5ocHg1Ej8ucFNeF1Y4s2KerO8Pq+Ln7Rkavl24Dr07NMY1Z7RNPfGjqurde/bseXbdunV7xb8rAJlrmvaYFRLcKOMl8fPwa79i9aZd5c6fW8VDVvBa7c/pcoX7I7jhmVkHL34V/VHmx2nU5bVP4kcelm61ZOWLdMOWAtz7f78YJr044jhUyUgj8eMWQWX0Y4UzK+bJ+v6wKn4+/mElPp2zGp1a18MtZcx4eH7Nj6qqqxRF6ZaXl7dV/NtE/LSyQoIbZUj8uIFyYn2s+XMXHnz11xKNkPhJDFM3a5P4cRNtOX1Z+SLN+2M7nny34qsJaKu7HD6stGKFMyvtuC1+vl2wDm//T0PrZrVwz2XdUi/zYwVUL5Yh8eNFVkraNHfZJkyevhzVqqRh776I8SGJH+/zFrWQxE/qcBW19KMfViJ//U4M7d+hzIyOKDcv909M/GQZGh5eDY9f37NMJ0n8uMd9qoqfucs3YfKny9GobnU8NvjQK1I8n/kpTXG/fv3SN2zY0KioqMjIhVapUoVxzqtwzo8OhUJvuxcSFfdE4scrTJRvx7TZK/HZT6vRumktrNiwk8SP9ykrYSGJn9QiLKLrxjRzUYRj5H87o22LumU68L/5a/HuN+Fyf7GLSiR+3OM+VcXP0lVbMeb9xTisWgbG3dI3tTM/OTk5p+i6/jqAQ/c+AgWaptVyLyRI/HgFa7t2vDDtdyzQNqNPxyYQ5/1Q5scuksmpR+InObjb7XXj1gLc89KBtTwjL+qMtllli59ps1fgs5/+wFGB+ri5f0fK/NgFXFK9VBU/qzftxMOvzQdjwEu3Hw9F/CPmSanMj6qqv3HO1yiKMpZz/inn/CIAzRljozjng8Ph8DRJfCfcDGV+EobQ8QbueWkuNm7dg4HHZxuXKJL4cRxyqR2Q+JEKp+ONzc/7CxM+Xmoqfl77MhezF29Ev85NcfmpOSR+HGem4g5SVfxs+Xsvbp/4s+GcyPyIDFAqi59/0tLSuuXm5i5VVXU25/xhcc9XMBi8FMCNoVBIXHrqiYfEjydoKNcIcfGdSMGLs0SGDeiIsVOWkPjxNmWHWEfiJ7UI++THVRD/iaeizM+4qUuwKH8Lzu6dhXP7lr2Hhaa93OM+VcVP7L2NYs2PWPuTyuJnV1paWvvc3Nw/AoHAy4yxZZqmjWnVqtWR6enpizVNO/T2MvdipERPJH6SBLzFbtdvKcB9xdtpxVkidxT/QqAFzxYB9EAxEj8eICEOEyZ89Dvmhzabip9HXp+PVRt34tKTVZzQpTllfuLA2ImiqSp+OOfGze7iB+7dl3VFdrOSh2Wm1LRXMBicyTmfpWnaA6qq3grgJE3TzggEAicxxt7TNK2+FfIDgcAxjLGJjDEVwGJFUa7Izc0Nx9Zt1apV7fT09PEATgUgtgJ9kJ6ePnL58uUlrtQorz8SP1aYSF6ZaAq+Ts0qeOjq7gcPVSPxkzxO4u2ZxE+8iCW3fHSa2Szzc9uEn7B1Z/kXUor6lPlxj8tUFT8CoVvH/4gduwsx9IKO6JxdUh6klPjJycnpp+v6FwDu1XX9TUVRQgD+AJDFGPsoFApdbRYSWVlZVTMzM1dyzkdmZGRMLSoquhPAKZqm9Y6tq6rqZM55nYyMjKsKCwurpaWlfcI5/0zTtNFmfYjPSfxYQSl5ZT6dswof/7AK7bLq4Lpz2pP4SR4Vtnsm8WMbOtcrijsGxTSzuLqiIvEjfq2LcoVFOu68pAvUIw6nzI/rbJXsMJXFz30v/4L1mwtwzRlt0LtDkxKOpZT4EZZnZ2eLBc6Z4XB4ZXZ2dtu0tLQrdV3fnJGR8ZyVrIyqqqcBeErTtPbFSKSpqrqFc94rHA4fvN5bVdWXAIzXNG2xKKeq6pBikXSWlVgk8WMFpeSVmfjJUszL/QsndW2Os/u0JPGTPCps90zixzZ0rldc99du3P/KvIP9lrfmJ3adxujBPdC41DqNaAOU+XGPwlQWP0+8vRChtX/jwhOycUr3I1Nb/JRHeSAQODMcDn9mFhJiuowx1jsUCl0QLRsIBOYDGF3RbjFVVcWN8r9pmlbRFRsHuyfxY8ZEcj9/4JV5WPvXblx+ShDdchqS+EkuHbZ6J/FjC7akVIoeOBftvDzx8+f2Pbhr0lyj2Phhx6J61XTK/CSFsX87TWXxEz3O5IyeLdD/uNapJ36CweAFuq5fyBiL6Lr+dn5+/vSoF61bt26YlpY2DsAATdMOvQSmVOAEAoF7xVofTdMuj34kdo4xxiaHQqG3yoqzQCDwBGNsgKIoR4trNqzEohA/27cXQNcPpHntPNc+8Z1xINh9V3RD61KLteJp76FX52HVxl248rQc9EvgYtMrR397sNvX7j4xHhM8VVZwIhbCiR1fd13aBc3qH4YhY2cbNj57cx+IdUB+esTLq06dGkg0Hr2GSTQerz6jDY7t1NRr5iVkj984+3DmCkz/afVBTG7771Fo1/LQc37Ca//GqDcXID1NwUu39wMrdTZLtIEo97VqZJZ5gJ1V8N/9RsPX89aiV/vGGHx2O6vVyiznN86iTsryS9b3hziYdurMFejQqh5GXNS5Qs5e/SIXsxZtML73xPdf7CN2FI79YDE+G3NuyQOA4ogC2xWt9BEMBodxzscAWAFALDbO4ZxfGg6H3w0GgwM45xMBVGeMjQ6FQo+Ytamq6nDOec9wODwgWlZkfhhjj2qa9nFs/eLTpEX7/Rhj/wmFQhXdLVaiayF+zGwx+/y826cbX9BPD+2LYDmnoZq1IT6/dews5K/9G0MGdMIpPbKsVCmzzFkjPjn49+nPnGO7nWRX3LBlN6577ICQe+uhU40X7CX3i8Qe8Mq9J6NBnUNvkU62zdT/oQj8P3vXAR5F8cXf7KVAIPROgAC5vRB6780Kil1sfws2QEWaigU7VpQiRcECFlTsvSNSpXdIcnsXeu8lBEhyO//vbW7xuFzZ29u9293MfJ+fmpudmVdm9rdvXpH1cdjANnB5l0aMRQbmwEuzVsCKLfvPr/CFwV2hnaNWqRX/u3EvvPrRKqhRpTzMfuayoBTJsq+SmgyfPI8xKera+z9shh8W5UHf9mkw+rb26gZhTynigFbvj6/+FuDjX3OgXWYteOH+wOVP5AV99Es2fD3fBd1a1YUn7+p0wTpXZe+HFz9YYVzww/N8NiHkL6fTOQJXbrfbHyOE3AYAbwPATABYQgi53+l0ovNz2Mbz/BUA8KogCK29ndHnB605XQRByJUH8DpGfwcA1Twez1V5eXkHww7u04FZfiLhVmz7rnMdgre+2gipKYkwdWQvyC8oYpaf2IpAk9mY5UcTNsZkkMff+RcOHDtzfq5glp/5a3fDx787oXHdVHju7gtfVr4LZZafmIhNmsTMlp/flu+AL+a7IbNhFXji9gvBrRksP6dFUewgOyOnpaWVT0lJOQUA+A9aayZEogbe59GCMyYhIWEuRnsRQq5xOp0XcIbn+fcBoHl+fv7Fe/fuLYhkDuzLfH4i5Vjs+v+6fIdkNsVIEowoyT9TxHx+Ysd+zWZiPj+asVLXgc4VeeDBCQvB1xQezOdHToTYqml1GDlQ/j4tvTzm8KyryC4Y3Mw+P1i2aNavOZBWswK8eG/nC+gyfLQXz/Oix+Op42t54Xk+n1L6vMvlelONCmRmZrYXRRGvs/AScL0oioPcbncez/Nb8PqsqKjo54SEhKMAUAQAxT5zLBYEAaPFwjYGfsKyKG4d3v85G/7dvF+6B0aHZwZ+4iaKqCZm4Ccq9sXs4R37T8ELH64C9I9ITrLB2UJP0AzPn/zhhH/W7ZHq7d1zRbOga2TgJ2bikyw/1atXhCOxVdhOAAAgAElEQVRH8qPyYZVlhiuf9cRFqgn4Zdl2+GbhVmjRpBqMvim0z89612GY8s1GqFIxCSYO62EJ8IOZntv5JyZUzU0dHmTgRwemajTkuI9WSQ7gt11ih0s6NGDgRyO+xnoYBn5izXF18y3dtA8++CUHalUtDxjKfqqgKCj4CRWd4zs7Az/qZKHmKTODH/fuE/DKnBIH+pmP9r7Agd6slp9TlNLWmOtHjTBj8QwDP7HgcuRzoB/6gxMXAZriMVKgeXo1Bn4iZ6MhnmDgxxBiCLuIr/5xw28rdkpV2t17ToQEP/iiwhfWLRfb4bKODZjlJyx39e9gZvCz78hpGPveColJ74zuLVke5WYK8IMOygBw2kfMzwDAdADAq6nzTWn2Zf3Vhfn8xILHauY4cuIsPPbOv9KjEx7qLoW1s2svNZyM/zMM/MRfBkpWMPmrDbAx7wgM6NZICjsOZfl5cuYyyTF68NVZ0CWrDgM/Shiscx8zg59TBYUwYsoSiUNvPNANqlcuZyrwg8khlISNU0EQApcA1lk5Ag3PLD9xYLqCKTdvPQITv9wA5ZMTYNrInpIZlIEfBYwzYBcGfgwolABLkmt1Dbm6OXw2TwgJfh6atBDOnPPAY7e0gWbppfMAycOza6/Yyd7M4Adzut0//h8JQDw3qCM0qpNqHvATOxFrOxMDP9ryU6vR/ly5E+bOd0PTepVg7J0dpGEZ+NGKu7Edh4Gf2PJbzWy+5SpevLcTvPH5uqDgp6jYA0PeXChNM+7eTlC/ZkVm+VHDdI2fMTP4QVY8PHkRnD5bDI/c3OaCxJqGv/bSWI4xG46Bn5ixOqKJPvwtFxZt2HtBNAkDPxGx0DCdGfgxjCiCLiRv7wl4+eM1YOMIvPNIb3hk+tKg4OfwiTMw5p1l0lhvDe8BqSlJDPwYQMRmBz/yVSpaHjtn1WaWH711ioEfvTmsbnzZofKmvhnQr3NJoTsGftTxMt5PMfATbwmEnx8/NPCDo16NCvDSfZ1hxJTFQcHPtn0nYdxHq4EjBN4d00f6d7DGrr3C816rHmYHPy9/vBry9p6E/13Kw8Xt0xj40Uoxgo3DwI/eHI58fIz0Gv7WYskEOnJgK2jVtAYDP5Gz0TBPMPBjGFEEXcjn81zw1+pdUvHgB69tERL8YMbdKV9vhMoVkqQae6EaAz+xk73ZwY/scH9tj8ZwdY/GDPzorToM/OjN4cjHP3G6EEZNLfH8Hz+0q1Q/iFl+IuejUZ5g4Mcokgi+jglz18GW7cdAfvGEsvzIVqIGtSrCC/cEL22BszHwEzvZmx38yEltL2mfBrddyjPwo7fqMPCjN4cjHz9nxzHJ4TIpkYO3R/c+b1Zn116R89IITzDwYwQphF7DqGlL4ER+oWT1QetPKPCD1bq/XbRVckpF51Rm+TGGfM0Ofub+7YI/V+2CLs1rw+CrmjPwo7daMfCjN4cjH//vNbvh078EaFQbiyZ2PD8AAz+R89IITzDwYwQpBF+D7756+f7OULd6hZDg57O/BJi3Zjd0bV4H7r8qi4Efg4jX7ODnp3+3w3eLtkKLxtVgtA+oZtFeOikYAz86MTaKYef86YT5a/dA1+a14X6fLwAGfqJgahwfZeAnjsxXMLWw6zi89ulaSLCVRHrZOC4k+Jnxw2ZYmXMQLu/UAG6+yM7AjwIex6KL2cHPgnV74OM/nJBeJxWeHfTfRy8DPzppDwM/OjE2imHHf7YWcnceh+t7NYEB3dKZ5ScKXhrhUQZ+jCCF4GvAAqVYqNTXhyfUtZe8Pwf2bQr9Ozdi4Mcg4jU7+FmdexDe/n4z1KhcDsY/0I1de+mtVwz86M3hyMdHZ2d0eh52fUtox9dk4CdyFhrqCQZ+DCWOUouRLa1dsmrD4KtLfC1CgZ+n318Bew+fhnuvbAbdW9Zl4Mcg4jU7+JF9Pcsn22D6qN4M/OitVwz86M3hyMYP5H8gj8CuvSLjpVF6M/BjFEkEXodsybmhdxO4smuJpTUU+ME0FLgXR9/UGlo0qc7Aj0HEa3bws+tgPjw3a6XEzXcf6yNVeMfGrr10UjAGfnRirMphXbuPw6tz1kqZZmc8WuJ/wMCPSmYa5DEGfgwiiCDLkMHMwze0hLb2EktrMPBT7BFh8BsLpD7P390RGtb+rwZToOFZqHvsZG928HPs1Dkpszg2zB+FeaQY+NFRfxj40ZG5KoaWc4jUr1kBxt3b+YIRmOVHBUMN8AgDPwYQQpAlnDxdCCO9ObVeG9oVanlzagUDP8fzz8HoaSUvqAkPdYeqqckhiWPgJ3ayNzv4CVYzjll+dNIhBn50YqzKYeVcD3KmWd9hGPhRydQ4P8bAT5wFEGL6nO1H4Y2560vl1AoGfnYeOAXPz14ljeh7NRFsCgZ+Yid7s4Mf5NTQCQugsEiEx29rC46GVZnlR0/1YeBHT+5GPvbEL9bD5m1H4eru6XBtzybM8hM5Cw33BAM/hhPJ+QXNW70LPpvnKhVeHAz8bN56BCZ+uQEqlk+EKSN6hiWMgZ+wLNKsgxXAz2NvL4UjJ8/BQ9e1hPaOkitYZvnRTEUuHIiBH50Yq3JYWfmHXtMcOjX7r7IvDscsPyqZGufHtAI/izfshWVb9sO9V2ZB9crl4kxVyfRavXDiRcxHv+fCwvV7oXuLOnDvgP8SFgYDP0s37YMPfsk5XwA13LoZ+AnHIe1+10oXZZnhymY9cZHqBf6ybDt8s3ArtGhSDUbfFDoTuDzJ87NXws4D+TCofyb0al2PgR/V3FfwIAM/CpgUoy5nzhXDQ5MWSbO9eE8nSKtV8YKZGfiJkSA0nkYr8CMfjP4vao2XG9FwWr1wIppUw86vzFkD7t0n4Ka+GdCvc8PzIwcDP7+t2AFf/ZMHmQ2rwJjb2oVdCQM/YVmkWQetdDGe4OfNuesge/sxuLFPU7iiS0kOKWb50UxFLhyIgR+dGKti2G37TsK4j1YDIQAzHukDiQn/RXrhcAz8qGCqAR7RCvxgGCyGw2Ik4GtDuhrC+qPVCyceYqKUwrDJiwE/OkYObA2tmv4Xth4M/Hw53w2/r9wJnZrVgqHXtAi7bAZ+wrJIsw5a6WI8wY+cPRyBOAJyBn40U4/SAzHwoyNzIxxaNqnXrloeXh3StdTTDPxEyFCDdNca/CBZl3RIg9su+a/yc7xI1eqFE4/1+4YWv/lgN6hW6b+rxGDg572fsqWrR//K28HWz8BP7CSrlS7GE/x88qcT/lm7B3q0qgv3XNGMgR891YeBHz25G9nYXy1ww2/Ld0Jbew14+IZWDPxExj7D9tYD/CQlcvDmg90lx9t4Nq1eOGiFIWjyjGGTnZcxo+60kb0umD8Y+JnwxXrYsu1oqdIzDPzEUHBBptJKF+MJfrCwKRY4bZNRA4bfWPIOYNdeOumWFuBHVpbhN7SCNvYaqlf64oerYPv+U3BXPwf0blNf9ThaKa/qBah8cMrXG2G9+zBc2bUR3NC7KQM/KvlotMf0AD9I4zU9Gkv/xLNp8cLB3Dl43du8cbXzX7uxoOmPlTvhi/luaFq/Eoy9o8MFUwYDP/LVo69Daqi1MstPLCRZMocWuojjaPX+UOPw/NeqXfD53y7ISKsMT93enoEfPdVHS/DjWxtHzZrLOvh5YuYyOHjsDNw3oBl0a1G6ZhC79lKjVfF/Rmvwgwkw9xw6DRXKJUjWn+QkW9yI1OKF89fqXfD5PBekpiTCW8PDh49rReysX3JgyaZ90Kt1XRjUv+SKQW7BwI9cdw+/yvHrPFxj4Ccch7T7XQtdjDf4wStVvFqtWz0FXr6/CwM/2qlH6ZEY+NGTu8rHxuyeQycsBEoBnh3UAdLrVCr1MAM/yvlppJ5ag59bL7HD94u3SY66+N+XdmgQN3K1eOHIFs9Ygx+0NmGQwa0X2+HSjhfyMBD4ESmFweMXAP776Ts7QJN6pfeovyAY+Imdamqhi/EGP5u2HoFJX2644EOAXXvppEMM/OjE2AiH9S1q987o3gG/5hn4iZCpBumuNfhBR8gDxwrgl2U7oFqlZCnySy6CGGuSo33hYK0srK11ttATU8sPApiHJi6Cc0UeePSWNpCVXi2s5edUQSGMmLJE6jf+ga5Qo3L5sOxm4CcsizTrEK0uyguJ57WXHPHLEQLvjekj+aEx8KOZilw4EAM/OjE2wmFXZB+AmT9ugeqVysEbD3YL+DQDPxEy1SDd9QA/LZtWhzHv/AtFxSLce2Uz6N6y9DVpLMiP9oUjF/LFtcbS8nP4+BkYM2OZxKJJw7pD5YoX1ugKZPnZcygfnvmgpOr2zEd7Q2JC+OtGI4KfwyfOgqNJDTh27DSIIo2FmsRkjmh10Qjg5+DxM/CEVy+njewJKeUSGfjRS3u0BD+N66bCM3d1VL3UsuzzI3v5t2xSHUbd1JqBHwsdynqAHwyF/eQPJ/yzbg/Ur1EBXri3E+DXYqxbtC+cH5ZsA/wn1uAHAwvwug2j5d4a3qNUpFkg8CPXAcPosOmjeititdHAj1w4GRf/4VMXM/ATQIrxtPwUnC2GYZNLEt2+NqQL1KqawsCPop2mopOW4AenjyYdeFkGP29/twlWOw/BZR0bwC0X2xn4YeCnlA7IkUZ47YXgB78Sn5y5TPITizbSUsXRIT0SLfiRMyzHGvz8unwHfL0gD/gGVeCJ/5XO1BwI/CzP3g/v/pgNtaqWl64alTSjgZ/XP10Lzl3HpaUz8BNYgvEEP5jyYfAbC8AjUhh7Z3toWq8yAz9KNpqaPgz8qOGa9s88/f4K2Hv49AU1XfxnYdde2vM9FiPqZfnBteNVKV6ZYrg2hsbGOldONOAHHbYfnrxYciCONfh576ctsGzLAejbrj7ccZmjlBoEAj+BwpDD6Q8DP+E4pN3v0eii7yriCX5wHSOnLoGTpwth5MBW0KppDQZ+tFORC0di4EcvziofF50+H5iwUEL7T93RHjLqV2aWH2b5CWv5wQ47D5yC52evkvqiBQMtGbFs0bxw5Ksneb2x9PmR66TdfhkPF7VLUwR+vlmYJzmZt+drwkPXt1TEZgZ+FLFJk07R6KKRwI/8ISynPGEOz5qoR+lBGPjRibF+w64VDgHmZ6ldNaXUhPuOnIax762Q/i47uQVaFbP8xEZWWs+ip+UH1zrxy/WweetRqTYV1qiKZYvmhfPZXwLMW7MbkhNtUtRVrMAPOvk+MHGh5Cz++G1twdGwqiLwM+vXHFiycR/0bVsf7ri8tLUoEN+1Aj+fzRNg3urd0DGzFjxwbfiaYsF0gF17hd8d8bb8vDZnDQi7T0juD+gGwcBPeJmp6sHAjyq2RfTQlu1HYcLc9dIzgXyi1jgPwvTvNkPlikkwaViPoGMz8BMR2w3TWW/w49x5DF7/bJ1E7wv3dIIGtSrGjPZowI/8hYugbWPekZiBnwNHC+DJd5dLPJoyomfAEiGBrr0mf7VBWmckmbW1Aj/3vjYf5LisaPwqGfgJvzXiDX6mfrMR1rkOw4Bu6VIZFQZ+wstMVQ8GflSxLaKH5EiuYOAHa7lgn2aNqsJjt7Zl4OdIvqWiUPQGP+gk+conayBv70no0rw2DL6qeUT6GU1nteDHt6gofuHO/Tt2GZ7XOA/B9O82QeUKSTDp4cAfG4HAjxyQccdlPPQNcFWmp+XH94X8/uN9VUf2MfATXtvjDX5m/5oDi30sjAz8hJeZqh4M/KhiW0QPhQM/7/64BZZnH4CL26XB/y4LXqmbWX4iYrthOusNfpBQvFad9u0m6aWIIbI1qoRPwKcFg9SCn6Wb9sEHv+RAlYpJUj2viX5ZbbVYW7Axfly6TcqQHepjIxD4eeztpXDk5Dl46LoW0N5RS9EStbL8+L6Qx97RHpoG8QsMtygGfsJxKL61vXB1X/3jht9W7IQOmbXgwWtbMMtPeJGp68HAjzq+RfJUOPDz/KyVsPNgPoT7omTgJxKuG6dvLMAPRkw98/4K2HekICyI1pIzasEP1i/COkbdWtSRrFUTv7gwpb+Wa/Qfa8YPm2FlzkG4pEMa3HZJ4I8Nf/CD1rUhby4EDE548vZ2YE9T5liuB/jp36UhDOyToYpFDPyEZ1u8LT+/Ld8BXy3IOw/OmeUnvMxU9WDgRxXbInooFPjxdb4cc2tbyGxU2vlSnoyBn4jYbpjOsQA/SCw646JTblICB+Mf7AaVUpJ054Ea8INAYvT0pXAiv1Aq4lupQlJMwQ+CxD2HT8Nd/RzQu039gDzyBz++yedeHdIlYOBCoIH0AD91qqXAK4NLil5G2hj4Cc+xeIOfxRv2wuzfciXfPfThY+AnvMxU9WDgRxXbInooFPjxTWc++eEe0osgWGPgJyK2G6ZzrMAPWiUen7EM0J/mqm7pcF2vJrrzQA348S0TMXFYd9h9KD9m4EdpWgl/8LP/aAE85XWSnj6qF5RPTlDEWz3AD0788v2doW71CorW4NuJgZ/wLIs3+FknHIKp326CqqnJMOGh7mUT/Njt9s6EkBmEELTNbuA47q6cnBxXIPFlZmZWF0VxDcdxfXJzc7eHF3FJDwZ+lHJKfb9Q4Cdcmn3fWRn4US+DeD4ZK/CDNP65cifMne+GCuUSYPwD3RS/pNXyRw34+XPVLsnBGctyjLuvM2zediRm4McXeE0b2QtSygUGMf7gR9h1HF77dC0kJnAw45HeipNJ6gV+buzTFK7o0ihisTHwE55l8QY/sq6hBXfGo33KHvhJT08vl5SUtJVS+mhiYuLXxcXFTwDA5YIgdPcXH8/zWFDrQwDI4jiuMQM/88+zKJqw0PDbRFmPUODntxU74Kt/8sCeVhmevL19yAEZ+FHGb6P1iiX4OVtYDI+9/S+cPlsMN1+UAZd3aqgrO9SAHzlkXPa5iSX4WZlzAGb8sAWqVUqGNx8sdZSe55U/+FmdexDe/n5zyMLDgRitF/hpWq8SjL2zQ8SyZeAnPMviDX4w0z+mgcCGQDtnxzF46+uN8PPEa1UX71P9YHh2ad+D5/n+APCGIAhyRisbz/OHKaXdXC5XjjxjZmYmL4riYkrp44SQ2Qz8aOetr5VUQ4GfD37JhqWb9kPvNvXgrn6ZDPxUrwhHWKh7QD3wr+0VTFlkfUOz+etDu0KCjdNKlUuNEyn4wWsnLGmBSQ1H3NgKWmfUiKnlR+ZNiybVYPRNbYLyxR/8zF+7G+b8KUDjupXgmbuUgw69wA8uHK8Mq/hVow8naAZ+wnFIu/fHL8u2wzcLt0I4XfNfkVTaYuoS6c9vPtgNdh3ML3PgZxQhpLvT6bxRZo7dbl8NAK+4XK5v5b9lZWVJGc2ys7PzeZ6nDPxop7zht4myHqHAz0sfr4ate0+ez+YZakRm+VHGb6P1kl+Ag/pnQq/W9VQvTyn4OVlQCGPe/hcKi0W4+4pM6NlK/ZzhFhsp+JFN+jaOSAkG0Xcmlpaf6d9ugjXCIejXqSHcdFHwiCl/8PP94q3w49Lt0CajBgy/sVU4tpz/XQ/wg6AW/bru7OeAPkEctoMtkIGf8KKLt+XHI4pw//gF0kKfv7ujJOsyZfmx2+1Po6+PIAh3yuLieX4RIeRdp9M5J5AI1YKfY8dOR5VUbtArf59fDlYKVttemL0Stu07JRX37NM2cBSGkrG1Wo+SuZT0+XZhnnRwYvPlD0a9YE2vs4UeePSWNtCiSfWQw+UXFMGwyYukPpicDQ9BKzV8kVatWgGi1Uej8UTWxy5ZtWFoFKUJMEoJvwLvHdAsLKCZ86dTKocgRQYN6aI6KV44XkYqM/wQ+GHJNuDTKsNT3mubzVuPwJtz10sZnqeO7BVuyqh+f2LGMkDn5XA8fHjyIjhVUCQlHW3euBp8+FsuLFi3B3q1qSflJVLaZNljIAOCPbXN90y7qF19mL92j1TOZPTNwa1XgeZ6dc4acO4sqer+8dOXRHXuq6VFr+ci1cVg69Dq/fHzv9vh6wV50LJJdXjklsjkhO8FLPyLEcCFHhEmf7mhTF17jaaUdnW5XANlIaHlhxDykiAI32sJfqJVxqse+eH8ED9NuEb1cKMmLwT3ruMwbGBruLxLuupxtFqP6gX4PTjn9xz44i9B+qsvfw4fPwN3j/tT+vvsZy4Lm5gOzaH/e/Y3qf+spy+DmlVjk8hOKz6U1XG00sfhE/6BbXtPwoib28IlYXx5sITD4FfnSS+3pwZ1gq4t6xqC/Y9NWQS5O47BbZdnwq3eauprnQfhuXeXSeVd5ryAt/36tMIiDwx88mfAmrkTR/YCe4PgaSVuf+43KRT/hcFdoZ2jFrw8ewUs37wfBl5shzuvyFK8QFn2VVKT4ZPn+yl+zr+jrw69OLgrPPvuMuk689MX+0FKuUTF4z759hLYnHek1FmkeIAy0FGr/frV3wJ8/GsOtMusBS/c3zUizg1+ZR5gzccxd3SAckk2ePGDFWUK/FwBAK8KgiBXKkSfH9TaLoIg5GoJfqL90tYKKZc1yw+a+9/8fL2k3O8oiCBhlp+Izg/DdPbdHyhnpWHS/gREYvnBZ2f+uAWWbd4PTeqV+KkQor3bYyRf21KunEmLABMyjr2z/flEgbGy/Ow4cAqe+2ClxNaZj/aB5CRbUB3xt/zg9bR79wn436U8XNqxgWLd0sPyg+Ut0G8KLQOYAbhTVm3F62GWn/Cs0up9Fo3lB0upoDvEnZc7oFrlcmXL8pOWllY+JSVlGwCMSUhImIvRXoSQa5xOZ9CQILXXXtE6mGp1RyrXzgmVfCy86prH5+evVbvg879dip0omc+PEukbr4/v/ojG70epz4/Mgd0H8+HZWSUv+3AJNNVyLRKfn3WuQzD1m00S2J86sifYuBJH7Fj5/GBGacwsXbNKOXh9aLeQJPv7/OB1GebkGnpNc+jUTDnY0MPnByNYEdiuyD4AnbNqw5CrlddyYz4/4TVdq/eZWodnXOGkLzfApq1H4LqejaFh7dSy5fODDMjMzGwviuIM/E8AWC+K4iC3253H8/wWQsgrTqfzU19RMvBTwg2tlDf8NlHWI5jD80e/58LC9Xuhe8s6cO+V4U3pDPwo47fRevnqo5KUBsHWHyn4wXHksPJII06U8jAS8PPpnwL8vXZ3KafhWIEf9L/4dfkORU7L/uDngYkL4VyhJ2IQqRf4kUP20Yr41vAeiiP6jAh+MO/TidPn4IZeTQH1SW2LRBdDzaHV+yMa8PPeT1tg2ZYDcGmHBpCVXrXsgR+1ShDJc9EmOTx0/IyUVVZu0eTVKWuWn9fmrAFh9wkY2Kcp9FeQsIyBn0g02zh9fQ9TXFUk5RF8qVADfuToKhwHI0fwK1LLFskLZ+x7y6XaY7ddYodLOvx3dRQr8DPl642ASUWv7NoIbujdVLHlB4uIogMqtpfu6wz1aijPrKwX+MErLwRoxR4Kj9zcRnLKVtKMBn7wCnTIGwvAI1J46LqW0N5RUwkZAftEootGBz+fzROkgIWuzetAp2a1GPhRrRUhHowW/MgVaHEKJebkUDSUJfCDkV7D31osJaPD0FkMoQ3XGPgJxyFj/u4PftSWnlADfpAjr8xZI/mr4CE69Bo5bZg2vFL6wjl68iw8+va/0qT+pRliBX7GvPMvHD5xFgZflQVdmtdRDH5qVil//gMPI7YqllfuYKwX+MHFy1cjfdvVhzu8zuPhpGo48CNSuG/8P9Ky0cLx6C1tw5EQ9HeluhhuAiNYfn5cug2+X7xNihTD6L4yFeoeTkBa/R4N+Ckq9sAj0/8FfCljq1WlPLw2NDKvdl86yhL48U1k9dqQLlCrakpYkTLwE5ZFhuzgD36qV0qG1x/oFnH4uVrwI5dQQX/nV4d0lfapVk3pC0cuuorpGTBxm6/zdSzAD15Z4dUVNiUWMN9rL3SMfvnjNYC5iWY+1iciuekJfhas3wMf/+6UUl748zSYfI0MfgIB40j0VKkuhhvTCODnn7W74RNvUs2ru6cz8BNOaGp+jwb8LN20Dz745XyyaQZ+ggggkM+Pc+cxeP2zdVKtoHdG91Z0183AjxoNj/8z8mHajq8J6PRLKcBjt7SBZunKripkCtSCH7xawCgnrGTet219uONyh2ZMUfrCefenLbB8ywHo3qIO3DvgQv+2WICfbftOwriPVkvA5Z1HekFiQvBIL2SOL/jBbNToqF2lYhJMHNYjIt7pCX6O55+D0dOWSuvBaD7MPh2uGR38yCVPwtER6HeluhhubCOAH9mnCz9Ubr3EzsBPOKGp+T0a8CNnJ5bnZZafwBIIBH5kZN+wVkV4/p5OikTHwI8iNhmuk3yYovkar1025h2Bbi3qwH1+ICDcwtWCHxz338374P2fcyTH2Dce7AaVKySFm07R70peOHjFO2raUkBr5/1XZUl+DL4tFuBHtjxJSR8HdwlLmyyzIdc0h7PniuGj353QsHZFeP5uZXtVnkBP8INzvPzxasjbexIGdGsE1/cK7ceE/Y0OftCBe+JD3UOmIQgmPCW6GFbwGgbMROPwnL39qJT4MyU5Qdoz7NpLieQi7KMW/GzffxJe/BCrbfzXGPhRDn4+/UuAv9fsjihUlYGfCJXbIN19wY+jYVV45/vNkJTIwaRhPSLK+RMN+MGaWk/OXAZHTp5T5PCrlHVKXji+IfeThnWHyn71qGIBfr6Y74I/Vu6SHGrRsTZck2XWqE4qtLPXgO8Wb4u4RhPOoTf4weg1jGKrX6MCjLuvcziyDA9+kAC1qU6U6GJYBhkE/Ow8cAqen71KWu7D17eEqd9uKjtJDpUISYs+asHPrF9zAL+mME09RixhY+BHOfh54/N1UrVezONwVffGikTJwI8iNhmuky/4wUrreFWBju6R1t2KBvwgU/5avQs+n+eSABf6iKhNtujLYCUvnD9W7oQv5rshrWYFePHe0i/oWICfiV+uh81bjwL6T1zbs0lYHZFlllazIjgaVJFC9NVY6/QGP5gFeOx7JRXAXx3cBWpXC+07aGTLT7NGVaUzEa3hz8lizMwAACAASURBVN3dMeKknEp0MazgDQJ+fAMEsJwKvm/LTFV3JULSoo8a8HP6bJF0gBcVi1KCLUy4xcBPcGkEuvYaNW2JlD4fM7R2yKylSJQM/Chik+E6+YKf2y9zwCd/OOGfdXuAb1AFnvhfO8XrjRb8oNPvY++UBCgM7NsU+ndupHjuYB2VvHDkqKTLOjaQCvj6t1iAn0emL5UKRD5wbQvoqGC/+YKfutVTYFXuQejXuSHc1Dd4MdRAPNIb/OCccgoBXBuuMVQzMvjBs/Dt7zdLy3/q9vaQkVY5Iv1UootKBjSCzw/6mcnpFVCuX/7jZuBHifAi6aMG/MhfclisD78gB79RUoGWWX4Cc94f/BScxQKli6XOkeQNYeAnEs02Tl9/8INp69FfDhtGRyqNvooW/OB8Py7ZBt8v2SbV0Ro/tJvkcB9NC/fCwes2LMZbWCTCyIGtoFXT0ikd9AY/UlkNb0FgvBrCK6JwzRf8VCiXAM5dxyXgEw5c+I8bC/Dz1QI3/LZ8JyhJoGlk8PPiPZ0Arye3bD8GXZrXhsFXKc9cjXwPp4vhZC7/bgTwg2sZ8uYCycBwRZdGUnJOZvlRKkGF/SIFPxg58tS7y+HgsTMwoFs6XN+ryfl7bQZ+lIEf954T8MonJaGzWOsJnVCVNAZ+lHDJeH38wQ86AD/9/gop4Z/SaxikSgvwgzr06NtLJTCC5vQeraIreBruhSNHNaKuY0mLckkJpQSkN/jBHEeY6yiS/eYLfjyiKMnq/gFZ0LVF6PxA8QA/eXtOwMufrAHMjTzp4R6AH6XBmtHBD5YQmfbtJkiwEXjzwe4hafGnMZwuKj0ZjAJ+ZGtlr9b1YNGGvQz8KBWg0n6Rgh/5oMKcIW880A2qVSrHwE8YZvtbflCRP/wtF9Cc/vL94SNP5OEZ+FGq1cbq5w9+cHW/Ld8BXy3IgxqVy0nWHwzBDte0AD84Bzpc4zVOsGuocOvw/T3cC+fbRVsBCzyGuuLTG/wsXL9HitaqX7MCjAvgcxSIXl/wc+zUWclHK5JMyv5WBAQkkx+OLEzed12hXsj4QfrItKVw4nQhhKsdZ3TwU7dGipRQ8ujJc3BD7yZwZdd0xeoYTheVDmQU8CPv9/Z8TVgjHGLgR6kAlfaLFPzIKeIxZ8mw60uiJmRlYZafwFz3Bz+RRp4w8KNUm43ZLxD4Qf8TtMBgzh+lRUe1Aj9Y3BOLfMYC/MjpMK7t2RiuDuLYrzf4+ewvAeat2R1RhmtZZhgav/9ogaRYSpIjxsPyg3N+/HsuLFi/F1o3rQ4jBrYOuhGMDn7SalWEn/7dDnhmSslAh3ZTlAMNCbYa+JGDYtDhHq9d2bWXxud7JODn8ImSOl54YD9ySxto7k3SxsBPaKH4gx/ZATTSMgfM8qOx8sdouEDgB6eWI5CUFrY1G/hB37aH31osnRdj72gPWCMrUNMb/KiJrJRlVqF8Apw+UywtO1CYfjgVioXPD64Bc0dhEVu8Qp8yokfA60XsZwbwgxasR6cvlep9PXxDS2hrV1bvy2rgB52/V+celCyWew6dZuAn3GaL9PdIwM83C/Pgl2U7pHBKrM8jm+q1Aj8vfLgKduw/pTrPg7+pGf8/mkKrkfIyWH9/8HO+xtDVWdAlS7kPgZbgRxQpnDpTpFmyOy14hc599epWhiNH8gHXZ5UWDPzIWVyTE20w6eHuQV9YMh/MBn7WCock/w0MqccXso0L7NumN/gZOXWJlGARLdVosVbSfK8+sD9eSr47pk9QGoKNGSvwg3tn+JTFUuX5h65rAe0dgSNItQQ/eB6h7kbjNI/7XK7thQ7PaPnBhhHEK7IPQIvG1WD0zW2UiMxylp+P/3DCgnV7pOAEjAxmlh9FaqC8k1Lwg5sLzfSnCorg1ovtcGnH/6oyawV+fBOLPTeoo3Ii/HpqdWeregF+D/qCHyxlEUmNId+htAQ/Mo8w1Br9MeLd8EU5/btNcNMlPPTv2KBMgB+sjTdy6lLACt33XtkMurcM7XxsNvDzyZ9O+GftHmhrrwEP39AqqIrpCX5OFRTCiClLpLmV5MEJ9AGFf0tNSYS3hveMeJvECvzgwmRfLsygjVmBAzWtwI9vHppoPjCDgR9h13F47dO1JXIb0gVqK6h9aDXLz7eL8uDnf3dIjvpoBWPgJ+LtF/oBpeBn+Zb98O5P2VJmWkw/nlLuv8rGWoMfXHE0G8rI4OfZQR2kzNj4JYmRXkmJoWsM6Q1+tK71pFY95XBdjgA8M6gjNKqdqnYowz0XzPKDC5V9NTIbVoExt4XO+WM28PPku8vhwNEC+N+lPFzcPi0u4EdNDT1cqL/lJxJnaV9CYwl+lmfvh3d/zAYMzceor0BRpFqBHzloI9qzOhj4wYjI52atgt2H8hX7plkN/Py5cifMne8+r04M/Gh8tCsFPxiajSHaGHaHEQWBNni0Ds9agRatxtGK1b6WHwyXfe/nbFU5kfSw/BgN/CDPsaTA03e2j/iKQSt5aT1OKPAjhynjnOOHdoUaISqumwn8HDlxVkqoiA2vyOtWD55bR0/LD5aQwVIykdbl8gc/mH34sVvbRqwasQQ/mM8IC7KilQDXimv2b2YBP7huvPLBqx8Ec29iva8wH4pWAz9yPT5Zhgz8RLz9orf8+NYZCRTxwCw/oXnsC36u7NpI8ptqk1EDht8Y/Cog0IhlBfwg7f5XqxqrfUyHCwV+8AsXyxNgRNG1PRrD1T2ClzoxE/hZvGEvzP4tF6pVSpZSYpAQofx6gh85m3aoq6BAyuAPfjpn1Zay2UfaYgl+cG0T5q6TkgRe0j4NbruUNzX4OVtYDJjr5sw5j6JSMFYDPxvzDsPkrzYyy0+km05pfyWWn49+z4WF6/dC0/qVYOwdHUoNzcCPcvCD/g/rXIehf+eGMDDCVPllAfzgtRf6Oicn2eDl+zpLeaTi1dDvAH09QlktlKwtFPjB5+Xqz+Fy/pgJ/MgOqz1a1oV7rmwWkk16gp/X5qyRag/e2KeplClXafMHP5d2aAC3XlK6NEe48WINfuav3Q1z/hSkMPHxAUCnmSw/yFu5ADRag5+9q0NIEG018JO39wS8/PEaBn7CbTK1v4cDPxiuOnp6SUZYdKLDLyj/xsCPcvCDkXLoB6HEwdV/1LIAfjo3rwNb95yAQ8fPhHWUVavzSp47eKwAnpi5XOr6/uN9FSUhDDZuOPCDzqOPvf0vYHzb47e1Baz8HqiZBfxg0r1RU5dIwRGDFUQ06gV+0Ko2/K3FUoLCETe2gtYZpUtrhJOZ/HukCffk52INfnwdkTFoBEGDbzMb+Nl7+LSUDR3b03d2gCb1KgXdvlYDPweOFcCT3jMIiWbXXkpO7gj6hAM/ciXoiuUTYcJD3QOGNTLwoxz8oPUf8548c1cHaFw3+EYONGJZAD8929SHzpk14c256yUWPHx9S2irMDw5ArUP2xXDbOWCvTMf7Q2JCcod04N9HFzUrj5gYdNAbcIX62HLtqNSuQksO2Fm8ON7TY6Ot5VDlFtAOvUCP8fzz0kFmLGF86cKJjP573dfkQk9W9ULqzfBxtEzw7P/nOM+WgXb9p0KWDrFbOBHkt1nayF353Ho1qIO3DcgcBQb9rMa+MEC4g97a0Ay8BPx1gv/QCjw4+uPgCZjNB0Hagz8KAc/cs/po3pJ+U8iaWUF/Nx7RaYUtosABH1GsPhroJpQkfAu0r6xBj9ypA5e900e1kO69vNvZrH8/L5ip1SFOq1mRXjx3k5hWa8X+Nmy/ShMmLte4iXuNyUlROTF+l97RWo58h8nluAHy4lgWZEGtSrCC/dcyH8zgh9M9IcJ/zB6bcJD3SA1JXDtMquBH7Sg3j/+H+ljmYGfsMdI5B1CgZ/s7UelL3AMy379ga5Qo3J5Bn4iZ7GUqh1TtssNX+hYtC/SVpbAz7GTZ+Gp91ZIOXC0KMMQKa9jDX4KizwwatoSybnzvgHNoFuL0jl/zAJ+Jn6xHjZvOwqXd2oAN18U3k9GL/Dz56pdMPdvl2RhRUtrJM0f/Kix1OJ8sb72wjn3HMqHZz5YKZH7+tCuUNMngtCM4KfYIwImhj2eXwgD+zaF/p0D+25ZDfyg/DB6D6+PGfiJZPcq7BsK/Ez/dpNUUC1cZBKz/IRmtj/4ad64mlQkMdJmRPCDUUrosIu5XKKxzsh5fvDaCy0/mP9DDnXFq8Jn7yrtvxAp/yLpH2vwg2vDYreYPyVYWLUZwA8mQ3148iIoLBZh1E2toWWT6mHZrhf4+fC3HFi0YV/Iq8Rgi/MHP28+WFLEOdIWD/CDFnvMsXTw2Bm45WK79PEgNzOCH1z7D0u2Sf9IQQFDugas92VF8DP2veWw70hJbTnm8xPp7gvTPxj4Qce5Me8sAzS9jb6pNbQIcYgx8BMZ+FEbOWJE8CPLPiOtMjx1e3vV2hkI/KDuvTpnDeTtOQnpUu6fDoqLHKpeiPfBeIAf9+4T8MqcNUEtrWYAPzk7jgHW0kqwEZg6olfA6zt/2egFfl7+eDXk7T0JN1+UAZd3ahiRSviDn5mP9lFVxiEe4AcJ/XK+G35fuROwKObj//sveaZZwQ8WAkbrD+YwGjmwFbRqWtp53YrgB88DPBcY+Ilo+yrrHAz8yNYKTFz4ypAuIe/LGfiJDPzc1c8BvdvUVyYgn15GBj+YgAwzVqttgcAPjrX7YD5gzTc89MJlClY7d6Dn4gF+8Iv9KcyKfOwMXNezMVzlVwXdDOBHrv+nJGO1zHc9wA/y8qFJi+BsoQdG39waWjQOb4Hy1QNf8IO+eegzpKbFC/y4dh+HV+esBbSaYlkODFjBZlbwg2uXC322alodRgaoXG9F8DPl642w3n2YgR81my/cM4HAD96xYugtVte9qW8G9Osc+quJgZ/IwI/aelplEfwgZ7/6xw2/rdgJ5TD3z/1doGpqcji1jvr3eIAf6evO66yKHx1Y08g3OaAZwI8caXRdryZwVbd0RXLQA/z4ZpjGKNVIdcYX/GB6CqwLpqbFC/zgtfHoaUvgZEHRBWk1zAx+5FIl6IP66tCuUpZ832ZF8DPrlxxYsmkfAz9qNl+4ZwKBH7naNFbrxYND/moINhYDP5GBnykj/vsSCycf39/LKvjBStXPfLACDp84Cx0cNeHB61pGwjZVfeMFfnxz/viDZKODHywiOnzyYilfUbicLL5C0QP8bMw7ApO/2gApyQkwdWTPkMnxAimIL/jh0yrDEyqvdOMFfpCm2b/mwOKN+y7Il2Vm8IPWPHTkxtw/gZLEWhH8yNeX0ofRxGsR96lqqh9UNZtJHgoEfrCaLma3VZKdFclk4Ec5+KmUkgiTVVSHxhnKKvhB2uWXGf43lgVBJ3w9W7zAD9L05tx1kL39GPRqXRcG9f8v54/Rwc+qnAMw/bvNUgqHqSN6KvbP0gP8/LZiB3z1Tx7Y0yrDkyqAiy/4iQZwxxP84HUJXpskJXDw1oieUm0sM4Mf3BtyrbaSvHPdLsi/ZUXwI2d/Z+BHh9PeH/ygj8Wzs0rCJJWGdzLwoxz8ROIL4T9qWQY/yAv5zh9T9790XxdFzrRqt0w8wc+yLfvhvZ+ypWs+TBIoF3Q0OvjBaDWM0GvH14Rh1yu3zukBfj74ORuWbt4PfdrUgzv7XViIWYlO+IKfUMkpw40VT/CD6RNGTFkC54o855OFmh38YOoLrDiA1mD/LPlWBD8Y/Yn7ioGfcDtNxe/+4EcuBBhJbgwGfpSDn77t6sMdQbL8hhNfWQc/GPHx9PvLpVw46IeG/mh6tXiCH3xZYXkIdNb1LSljdPCD0TgYXn3HZTz0bZemWDR6gB90kt+x/5RqJ3lf8BOu4GwoQuMJfnBd07/bBGuch85b8c0OfpAm+R2FpS7welVuVgQ/KDuUIQM/io8T5R19wU8oVK1kg6MD2mtDuyqf3K+n74Ez64mL4j6O6gX4Peib5yeaiKWyDn6QrbLZG7P1PjuoAzSsfWHtIq1kFk/wgzTIOWqy0qvCo7e0lcgyMvjJzTskBUlgQ+dgdBJW2rQGP5gi4cEJC6VcQ4/d2lbKmxRp8z2L7rzcAX3aRh6diXPGG/z8u3kfvP9zjuS3Oenh7vDm5+vBueu4xI4Pn7pYyqelpvlaJKI5q3H++8b/Iy3hxXs6QVqtimGXs/tQPjzrTeKIZ0B6nZIyQVYEP7KTNwM/YdUi8g6+4Ed+sVQolwATh2EdL2X1jJjlJzTffcHPY7e0gWbp1SIXVBn3+ZEZhofly5+sgW37TkpFDp+6o31EZQuUMj7e4Ad97tD3Dh0V3/Am2DMy+Pn2byfM/jU3aDXxUHzXGvz4FqWdPLwHVApSDiHUmnzBD17h4VWemhZv8IMfTCOnLJHytWHR3O8XbzM9+EE5nPdL9amFZ0Xw45utmzk8q9mBIZ6RwY/HI573pI/0SoGBH+XgZ9Kw7lC5orpQbaNZfny/2vTK8xOIs1g488UPV0sHeqRXLEq3T7zBj5Sld+ZyOHj8DFzfqwkM6JZuaMvPuPeXwcqcg9CzVV24O0hh1mC81xr8rHMdgqnfbILUlEQpx42a5gt+EGBn1K+sZpi4W35w0Zh0EpNPYqZnvAo0u+UHaQoUkRwt+PGIImzfd0r6uJJbNFYt2Vm5RZNqMPqmyDP64xpO5J+DUd7ivAz8qNqCwR+SwU/2tqMw/vN10pdmoBwKSr6S2LVXYC7JNYbw1w8e7xtx2K08qlHAD76YMZLk24VbYc/h09LysHI3OueqbcGSHAYb74v5Lvhj5S4psujl+ztDFZWAMtj48QY/uK6flm6D7xZvg9pVy8Mrg7vA87NXwa6D+VLVd6z+rrahMzU6VWtRMw1fOFWrVoDbn/0NTp0pgiFXN4fOWbUjWprW4EfOlRRNcIEv+MGrfP+cMkoJjLflB9c5b/Uu+GyeC2pWKQdVU8tJkbzYzHrthWv3zUUnZ/COFPzgOYYJRbdsOwpYxxIrx6Prh2+LN/hBOge/sUBaEgM/Snedwn4y+Jn27SbA6rnBsmcy8KOQoQG65Ww/Cm/MXS/9Es1mMgL4wYPz6wV54N5TknJdbgO6NYLrezVVzaRIwc/ZwmJ4+v0VcPTkOejUrBYMvaaF6rkDPWgE8IOJ+tCJGL0ysHTIJ386DQl+jp8phpGTFkpsVHPNpDX4effHLbA8+wBc3C4N/ncZr0ovfMHP26N7qa5bZwTw45vwEV0aTp8tecGbGfzg+s9XIfB+HGDV9+rVK8KRI/lBfZlOni6E7B0Ido5JgAfPD9+GGbHlKuro54X+XmqbFpYfnPvBiQul4AcGftRKIshzCH7c24/Ao9OXSiUERtzYClpHmEOFXXuFFopc7wgTrk1TmSYfZ4gn+MEUCF8vzJPy7citS1Zt2L7/FGBxU/lqRq16Rgp+cJ71rsMw5ZuN0pRKi2gqXZ8RwA+uVb6y6N2mHmzde9KQ4GfBhn3w4S/Z0LBWRXj+nk5KWXy+n9bgB51h0SlWC0dlXGQ0HyxGAD9Iw/OzV8LOA/kXyMbs4Me//mSrjBqlwA9GTrp2HZfAzpbtR6X949/QOR8DC5qnVwO0Fn78h1O6wg2USDES5dYK/OAHECZ4ZeAnEu4r6Ivg54PvN0qOcKEq5oYaioEf64Kfw8fPSFcvy7fslywQ2PAO+8beTaVIq0lfboBNW4/EBfzgWqZ/uwnWCIck3R13X+fzOXEUqH7ILkYBP3K0TvlkG1SqkAwHjhYY7tprMtYfEg5Bv04N4aaLIk8/oCX4Qb+NByYshGIPBbVlZFAxtI48rVQhCSZHcS0c7Xp+XLINvl+yzVLgx3f/Y9LTkTe1hipVK8DaLftg89YjkmUHLdSoC74NfcGy0qtBVqOq0r+rVy53we8zfthsKPDz4oerpI9MBn6iPdX9nh8w+nuK/hLH88/BwD5NoX+XRhHPwMCPOcAP3nGjlQa/gj79S5AW3bdtfbgjgGn3ZEGhVGfqn7V7JIsgNoyuQtCT6RM6HG/wg19/Y99fISU9u6JLI7ixj/qrN18pGgX8IF0jpy2R6JObkXx+ikURhk1cJIWVqykgijRpCX72HTkNY99bIbEKy1pUKFdS0DPSFi3YOC+r1+ZL/xlv8IMWD4wW9G1YYBkjT9X4M8Uz1N2XBgQ4b85dLxVwvbJrupRkEy3kvg0zXPMNqpQAnvSqUjg9psoI1owGfiZ+sR42bzvKwE+kmzhcfwQ/2AfvSzFdeGoUYaHM4Tkwt+N57YXFafGAKPnnGGCiQN/mn8ANHf7QQfv3lTvPv3DrVk+R/Hna8TVKOWvHG/wgLX+t3gWfz3OBjSPw3N0dIa1m+Fwh4faFUcAPrnPWrzmwZGNJcUNsRgI/uTuOSYESCTYCU0f2UmV50xL8oN8iZgKvUjEJJg5T74BvNfCDHz6Pz1gmXZ/4N7SaNm+MwKCalBMpXC1HfN4o4AfpQrCLH3VyQ1iTXjfVC3aqQUb9SorTtuAYRgM/sg9bmbL82O32zoSQGYQQ9NrbwHHcXTk5OS4/5eXsdvtEQsgdABj9Sye7XK6Xwx3u8u8y+OnWog7cNyBL6WMX9GOWn9BsiyX4QQsBhrLKgGf3oZJoLN9Wp1rK+cNC9vHCqAL8avrp3+1wqqDkywkrYV/TozF0b1kHbBwXkEgjgB8MuR/38WopjBdDkp+4vV3UuX+MBH58E50ZDfx8szAPflm2Q3ppYkJBNU1L8PPDkm2A/+DL/JGb1YUXSzz2Wmwk8KlBwtV4W36Qjrl/u6QPG7kh6PEHQwgcGtZJlfxf0EqCtdEC5XszCvhBWuSPH5muewc0g+4t1EdDGg38oJUec/CVGfCTnp5eLikpaSul9NHExMSvi4uLnwCAywVB6O57wDgcjhGU0lsTExOvOHv2bDWbzfYXpXSwy+X6S8lBJIOfsXe2h6b1ostlwSw/gTmuJ/jBF/+2/SdLohe2ldxxy9dU8mrO33GnV4WsRiV33KOnLYHj+YUw/IZWcKawWIqckA9CjAhBEzLWNEpKDJ3o0gjgB+ncvv8kjPtotRSpcWc/B/Rpoy4jr8wzI4EfzGf05MxlcOh4yVe7kSw/4z5aBdv2nZKuG/HaUU3TEvzI9d+iDeO3IvjxBdGN61WC5wZ1LLkG94Z64zklR4LJckzEK6O0ypCFlqFG1aBB7ZIrIyOBn4KzRVK9r8IiUVr24KubAwZjqG1GAz8yoC8z4Ifn+f4Y7CEIghzDa+N5/jCltJvL5cqRBcvz/ApCyBtOp/Nr/BvP848AQCdBEG5WInwEP/gF8PrQrqrzzzDLT2hO6wF+ruvZGHYcyAe8dijwy00h3XE3rCIdVvgFXL9mhVKWEBn8oIlbviPH5y7t2ECKckhR6CthFPCDEvhsngDzVu8GjKp7eXAXKfeQ2mYk8IM0+DqsGgX8oN6MeGux5Aj/7KCOkF5HXakRLcHP2PeWw74jBXB3/0zo2bqeWvFb0vKDzuCjpi6V9rsMfnzLW+B/7zhw6vwVuWv38VLOwnheoEXo9Jki2LL9mMTfaCxjaspbBBIqFv9EQGZF8CNXXihL4GcUIaS70+m8URa23W5fDQCvuFyub33AzwmbzdY9JydnM/7NbrcPIIS8IghCKyU7H8HPLRfbpUKRatugV/6WHq1VtTyMf6Cb2mFAHgcHQP8Ntc3X8hHNOGrn938OrRH49Z5SLgHeHt1b9bD5BUUwbPKiUs+j7x4WosU7ewQ7ePWDX2yhGqa8Ryd3bPgl16tNPemKC6+6ImnojIfh77iGUE6E4cbEQxBfoj3b1If7BzRTVXMI/ZWeene55NcU7Xr8rWfR6JE81kXt01TnDTl0/Mz52llo1u/ZSv2LHX0I/t28X0poionh1DZZr/GFGE0KB4zMQafVaPc9Pi/z+pm7OkBTlVmZcRzfswhDwtU2eRy89poyQl22aS3X8/7P2ZL/GIKfF+7pFHKfyWHiGCKOiQD9Q+VlnkSzN3xlhtGaDRTU9gokCwRtz3nrfd16iR0u76T+ffbO95sBP36i3R945uMeadmkOjxyi/orWIy0nfHDlrJz7WW3259GXx9BEO6Uhc3z/CJCyLtOp3OOz9+KKaW8y+Xain9zOBwXUUrfFQRBUcwpgp8vX7lSypSrtl31yA/So0/c1RG6R3Eoy+OoXYfRn0PT8evD1B+A6Jdzz7g/pZd73RoVoA1fE9rYawLmt6gYoaP60zOWwgbXYejRuh7c3r8Z1FfpJDz7py3w7QK3Zqy/vV8m3Hyp+sRiK7fsh5dmrzifqEyzhWkw0IQRvYBvGHmRTXnql2atgJXZ+2H8sJ6QqbI+HI71zXyXlJdHq3Z5l0YwbKD6wx3D94e8Oq/Uda3a9WH06ntjL1GdmBDnlc+iB29oBf27NVa7lPPjDOjRGIZcp+h7NOBcY6YuBkyWigEpn43DSwF1bVPeYXjq7aXQq019eOyO/yqiKxkNSy1scB2S0hos2bC3VDZkJWME64Pvn9nPXAYVyquLzsNxn3x7CWRvPQJvDI9un30xzwlzfsuNhpwLnr2uTwbcc1Vz1ePtPZQPD4yfDz++eY3qLxXVD6pedRQP8jw/mlLa1eVyDZSHQcsPIeQlQRC+l//G8/xJURS7ut3uLfg3r+UH+yg6jQ4fL6CcKKr60pbXgF+lmASvrcrif/I4RcUiYF4TtehfHocQAoUiQBKH2TrVVS2OQnRBHiUSXeEsMuHmxSuu8inJYKPRyaywyAOnzxZJ6e6jachfDKNFYBZtK5eUAC34WnD8eEFU+oiFLf3DXdWsLf9MsSSv5MTQVrRwY6PMatdIhdqVk6OiC/fHqYJCqFYpepntPXwa8Ms+2paQwEErRx04eSI6maEVEtMWaNEwaZ3aEHd5ftwbxwqKoWGNlKhkhhZNzNGCaSKibXl7Tkjj4PkWTcOPp/QGVeHUyTOqacN9jwEG6COEOaiibbWqpEDFFPXAB+fHtAsJSYkQ7fsMadtz6DQUFmuwO/0GawAAIABJREFUP2ycdO5HKzNMPdKkYXXVglf9YLSCVfM8z/NXYJktQRBae59Hnx9Mr9tFEITzsJTneUzegP2+w35en5+OgiDcomRe36ruSvqboU+kNV7MQJO8RkabmaRVslYmMyYzI3HAqvpoVbrkM6RGjVTVGEb1g/FQ3LS0tPIpKSmYknNMQkLCXIz2IoRc43Q62/uuh+f5UQBwi8fjuYoQkspx3DxCyAin0/mjknUz8KOES8bpY/UNHq42j3EkoXwlTGbKeWWUnkxmRpGE8nVYXWZlBvygyDMzM9uLojgD/xNLGYmiOMjtdufxPL8FnZqdTuenffr0Sdi7d+9rAHA7AFrXyESn0/m6UpVh4Ecpp4zRz+obnIEfY+iZ0lVYVR+tSpeVLZFWl1mZAj9KD6Bo+jHwEw33Yv+s1Tc4Az+x16loZrSqPlqVLgZ+otH2+D2L+sjAj8b8Z+BHY4bqPBw7lHVmsA7DM5npwFSdh2Qy05nBOgxvdZkx8KOx0jDwozFDdR7O6hucWX50ViCNh7eqPlqVLmb50XgDxGg4ZvnRgdEM/OjAVB2HZIeyjszVaWgmM50Yq+OwTGY6Mlenoa0uM2b50VhxGPjRmKE6D2f1Dc4sPzorkMbDW1UfrUoXs/xovAFiNByz/OjAaAZ+dGCqjkOyQ1lH5uo0NJOZTozVcVgmMx2Zq9PQVpcZs/xorDgM/GjMUJ2Hs/oGZ5YfnRVI4+Gtqo9WpYtZfjTeADEajll+dGA0Az86MFXHIdmhrCNzdRqayUwnxuo4LJOZjszVaWiry4xZfjRWHAZ+NGaozsNZfYMzy4/OCqTx8FbVR6vSxSw/Gm+AGA3HLD8xYjSbhnGAcYBxgHGAcYBxwBocMFVtL2uwnFHBOMA4wDjAOMA4wDgQTw4w8BNP7rO5GQcYBxgHGAcYBxgHYs4BBn5iznI2IeMA4wDjAOMA4wDjQDw5wMBPPLnP5mYcYBxgHGAcYBxgHIg5Bxj4iTnL2YSMA4wDjAOMA4wDjAPx5AADP/HkPpubcYBxgHGAcYBxgHEg5hxg4CfmLGcTMg4wDjAOMA4wDjAOxJMDDPzEk/tsbsYBxgHGAcYBxgHGgZhzoEyBn3r16qXs3bu3IOZcjs2EKEsam6nYLBpygMlNQ2ayoVRzgOmhatbF7UEry0x32soM+OF5/mNK6b8ul2tG3FRVx4n79OmTsGDBgmIA0F1pdCTjgqHbt2+fmJ+fX87pdJ6yEl1IpMPheKu4uHhqXl6eO1b8jMU8KLMzZ84kZ2dn51tNZrHgX5znsAGAJ85r0HR6h8PxKQB84XQ6f9R0YGMNxgGAaKwlRb0a3WkqE+CH5/nPAeBmAPhUEIQ7fIBC1BKK9wA8z0+nlFYmhFCO4+bk5ub+Ee81aTE/z/PvAUANAMgihDzjdDq/BADdN4QWaw83Bs/z3wNAfUEQOobra6bfvTKrRCmtxXHcY06nc7WZ1h9qrXa7/TaO43Y4nc6lVqEJ6eB5/kkA6CEIwpVeuiwDgOx2+xxCyG2EkJedTuczAGAJ2ux2++scx1UCgMOU0p8EQVhpFZ3kef5VQkgKpfS4zWabkZOTs08v2iwPfrwvmuoAMBEAhgmCcLFezIz1uPhVQynNoJRO5jgO//00ADxRrly5dzdu3Hg61uvRaj4vWG0giuJjNputM6V0IiGkkxVepna7/QdCSF1BEDrJL5v27dtza9asKdKKf/EYh+f5uQCQznHcc6IoDsFD2eVyzY7HWjSeU7Kk8jy/BQA24jkiCMIqjeeI13CE5/mX8cwAgI8FQRhkFQCE5z4hpAql9GsAuEQQhGvjxWQt57Xb7V8RQhoiXRzHpVFKca/d43K5PtNynniM5T0ba1FKf+Y47nqPx3Of2+1e512L5h++lgY/XuTfXBCEtt6vnJWiKA5yu93ZZjfJo/9ShQoVPuc47gGn07kX6cvIyLjKZrNNo5S+JQgCgj3TXYE5HI56lNKP8/Pzr5b9s7wv1nmCILwfj02p1Zx2u30AIeR9URRbut3uQzzPjyKEtKSUNiWEvOd0OvEAM535umXLllXPnTs3u1y5cv9D0I3ywq83URTPAsB3LpfrCzPShXKXrcQ8z68HgCQA+AcAPrQKAHI4HBdRSocBQCqltMDlcl3jo++av3C02kuhxuF5/gtCSIbT6WzftGnTWjab7bvCwsIrt2/fftyMZ6JMa+PGjWsnJibOKSgouHr37t1nvO+0uwBgFgAMEgThE7Nax3me7wEAU33e1SsopWsIISdEUfzR7XYv05o2y4IfVHqO4252uVxTUUmaNGlSOSEh4S8A+FwQhEmx2IR6zpGRkZHMcdxmVHxBEF6V5/K+YD+jlN7tcrm+0XMNeozN8zxedaHiP+1yufC6Ev1jvqaUOgVBGKvHnLEaMy0trXxKSsoflNK1ALCYEPI6ALyGV2AAMJpS+rjXJ81UoNVL1yYAQIsIAvH7CCHP4rUlpXQUAIwRBOFts7548EOjYsWKfxJCJlNKB1FKDxBCZlgBADkcjr6U0ucppWM4jnudUrpTFMUPOI47Y8brFIfD0RgA7nU6nWgFBy9gQL0c6wUHsdrums/jfYetpZS+5GtVdTgct1NKZ3Mcd2lubu4CzSeOwYAZGRldbDbbxKSkpCvPnTt3OQBMA4CPAKAeIeRqURT7u1yuRVouxZLgJyMjoyYyCb+u8d9ZWVlJ2dnZhTzP30wIeUAURTQTbtWSkbEaCw/ilJSUCl7LAaL+KwghM51O53x5DTzP3wcAwzmO65ubm3vUJFFgXHp6etL27dvP4voJITmyfwXP82gR2S4IwlNIY9OmTTNM5ijMtWrVqjxaRTIzM6uLorgG6cBN7XQ68SoF7Hb79YSQKQkJCR2ys7P3x0qfopyHS0tLS8avUJ7nL0bfLO817CCXyzXPC1yvoZS+5/F42ufl5e2Kcr5YPi4DUJKWllauQoUKLzqdzscyMjLSOI6bYWIAJNMlWXW8H1EzRVEcDgD4QfUnALSmlA70fjyZyU9GtlRJNCJtbrf7nMPhGCGKYseioqJhXutPLPUo6rlatWpVoaCgIAXPfLvd/jQhpLYoijPcbjdexUrN4XA8Lopit8TExP9lZ2ejy4MpIn+RNkpp0pkzZzAKuyneyvA8j76QewVB2OM9G8eihbygoODu3bt3ozVZE9osB368L8paANAeAKYIgvCcDyjIxDt7URTfcbvdP5nN8Znn+Q8BAB3d0FLwqMfj2W6z2dCRD0RR/NTtdi/0KkszAJh05syZ62TzaNQ7UMcBeJ5/F60EhBC88vnCZrP9gGDVR24fE0IWOp3OD3iefwQAniwsLMwww0HmS5soir/gFxvP8/3xSzshIeHhnJwcvIIVmzZt2sBms31QWFh4k9noAoDvnU7nHDRL8zz/NKXUJVvtmjdvXq2oqAgjbu4QBOGwjmqk2dB2ux19X5JcLhdes5a6hszMzEwXRRG/TPdwHPdRbm7uv5pNruNAAegiffr0se3du3cJWooJIfUA4FsA2IoWIL8rMB1XFv3QXtqSXS4XBkqgzM5f2WVkZPTmOG6S1zcGry9NA+h4nke/udoA0IwQMo4QMp9SOtNrZf3E6XQ6kXs8z18BAA/5OK5Hz1SdR/ChDYNaXnc6ne/4WYdlfzsMVrpFEITrtFySpcAPz/N4WDUrKiq63mazteY47mu09DidTjx8peaNbnigqKio47Zt2w5oyUw9x/I6ATcWRXEkx3Ej8NoErxKaNWvWyOPxPO9VmvmCIHzM8zze4Q9OTk7uvWnTpmN6rivasb0bIItSihu7IQC8SQiZWFRU9MbWrVtPIF08z/9BCMHrocaUUrziu9IMVw6BaAOANzweD/r9FKL+8TyfKQhCLs/zD1FKhyYlJfXesmULWusM2wLRRSmdUr9+/af37NlzOSHkZkrpFy6X6xe73T4UD2WbzdYnNzf3iGGJ8lkYz/M/U0rrcBw32el04tUrhn/LL1Pp3959h4BvXWFh4Ri0WBqdtiB04ZmIFlX8oLoRAEYQQhbhC9bj8TxoFmtdGJmhZXUSIeTS5OTknkY/E33eVejDk46BOoSQFpTSTziO60gpLUcpfYEQstbj8cxzu91/2u32h3HfEUL6e1ODGFodeZ4/TxultDkhZA7Hcf3laGW8vUlMTKydk5OzGc9GdFovKCi4jVl+Aog1PT29XFJS0qccxz2Zm5srYBeHw/GSKIoVXS7XSMw/IkfUeL3KqwiC0NdrQtPEjKaXtnmd9hDIXYmKzfM8+h9UpJQm4pUCIWQ9pRS/boZRSvNww4iieKPb7UbfEsM2vI5Eq0BCQsJTOTk5Llwo3v1yHPcpIeRz7709gh/M0YFWu2qiKF5qdLqQjiC0dcV0BISQz5xO53MOh+MqBH2U0iOEkExRFK80Om2hZIYRQ6IofsVxHPr54JfoVgS0Ho/nWp+oDcPqo49zM0YKYdQJniP4QYEgB60JF1wZobUOiTE6QAhHl91uR6vPB4SQm5xOJ0ZH2dLT0xPNAOjC0Sb/jnpbXFyMPpDHBUG4U6urE72UGX0fCSF4Dt4mfzTY7XaU0RYMZrHb7b0IIQhW0T8Gr5Px/Lja6OeH1wBRijav4QJpm5SRkVGJ47hXKaVI4268xaGUXuZyudBqp1mzjOXHmxBvOaX0B0EQXkQO2e32F9HrXxCE23w5hqiS47gk+U5RM27qNJDXTwSdte+mlKLMvuQ4DmnECI1xAPAyKg1eMRQXF1emlJ4yyxUDz/OrCCEL0J9CZp/dbu9MCPkdAJ4RBGEa5rUghPzPZrP1wy8Bndis+bChaCOEPOJ0OmfhIWaz2coXFxdvcbvduNEN3wLR5QWtvxNCHkJLa0ZGRjuO4yoQQvLkaETDE+ZdIM/z8yils3wi8X4OBoDMQpP3peNP1y9eujx2u72J1w/SrBFeYWXmcDg6UEr3meHcz8rKqlhcXLyUUvqOnJjXe4VeKAgCWvYB/WXOnTtXixBSjeO4PWbxFQxGGyHkjNPpxFsN/AjGCNj6SJvNZluXk5OzQ+u9ZhXwI32R4YvEe1cvOVvyPP8KOlEJgoB3hgiGOiclJbmMfq0QSMjp6elV0BcEPf7Lly9vk2nwfgF87vF4epvMCViW2fV4n4smXfTDkml3OBxXU0rHJycndy0sLGwKAEecTuc2rTeATuOFow2dgMcnJCT0NsuB5eVTSLp4nsdcKghU+5oN8Pjqgd1uH+5yuaZgFFuFChVeoJQ2AgAZKPhagHRSH32G9adLFMV0QgjShVcQsp8MWsENbQkPxB0FMtOHqfqNSux2+y2EkF2CICzxvs/QreOcIAh4DQTNmjVrYaaPQR9WhaXNbrc3c7lcOfqxt8SMa5mGV1++plqHwzFOFEV0XHyc5/nRAPCCzWbj9cwaGQNmXhAG7XUoxfvSO8ziU+HLoyZNmjRMSEh41GvF+hr9RLwbG32ZZiUnJ99oljt6f9mHoQ2dm280g3NzWaErUB4Rh8ORKooiRtg0oJQuCOYEHYN9H80Upaw5FqELeWJZ2tBC4i0TI8ne4XC8g1exaOX3vs/Q+p9uFiu/rwIroU0UxcZyxHY0yh/sWdOCH59wZ1n5S3nw8zyPXvGrKaXFhJDxHMf1y83NlcKMjdzC0ZaVlVWnqKion8vl+shutw9Bp24AuNhEm0CSmeyH5c3N8TilNBkA1qSmps48derU/QDwMAD0NBFd5w9jC9JmeZkFiwJCoICO9pi4saioaJTXEd/IR4i8tqBno/dlala6fEFPwMgts8vMLxJZjnr6BvP5AEBNjI4ihFxhsqz3kj4ahTZTgh+e57/z1kaSSwScR//eq66NgiDMtdvtbxNC7gGAU6IoXm4SZ7CgtNnt9tfQ4c0L5vBKDxPK1RJF8SajO5RmZGQ0T0hI4HJzczEZHvg5oA8lhGBEDWbQfRCvuDC8UxTFW80gM6vSZlW6UP9C0YYRoYSQFd7cWdLZgl+q586dS8nLyztoZNRjVbrKsMyeIISsRF30pnHB8kwJHMddZoYP+TD6GFfaTAd+eJ7HPBQIenK8ab7PJz3ylrNol5qa2hoju+x2+62EkOdtNtsNZrgbVUBbe0EQMIePlLE6MTGxGiHkpNGvu+x2+5cY9UMISRRFcYXL5UKAI5tysT5ZB0EQHN4DDhOt1UhOTi4ww3WXVWmzKl2oY6Fo854hqI/NfSqcm8IJ2Kp0lXWZpaamtsT3mZymxWazXWGG95kSfYwnbaYCPzzPo0MsJvm7AQD+ppQ+4pNJ9n+U0gdTU1P7yCHtmI3VZrOJZnC+VEJbQkJCX0z+52s1MfJXKK7Na4nrm5ycfMXZs2cHekO6n8TMq3a7fTAhZHhCQkI7s9FlZdqYzEr0UetaQnru1UhkZia6It1nZqItQpmhg7OdUlqUm5u7XU9d0mJsM9BmGvDjDVvvLwgCpr5G569ZoigulmuceO8RMWLB/05RC1nqOoaFaSMOh2OyKIrLMeOv3W6fTAjBHBvoxX8Sq0kLgrABmWu2bNuY88WitFmVLlQzq9JmVbqYzPxcBHR9EWk3uGJ9jOeHvGnAT2ZmZjffNPJ2ux2LXN5SqVKldrKlxys7UxWFxDVbmTaHw4H1nrDEyM+YYZVS2o9SimUOXuM4Lq1u3bqdFyxYUKzdvovdSFalzap0eT+aLKmPTGbmO0OYzOIrM8ODH3SYSkpKOpKdnY2lKKhcpBQT/6HnuyiKH5mxernswGdF2jBHg8fjOb1161bMPEp5nseMvwMopd+7XK6pMjzheT6bEPKKty5U7FBLFDNZlTar0uX1F7GkPjKZSdfqpjpDmMyMIzNDgx+Hw/E1pZQnhBzFMGiO426V7zvRXHbq1KnJlNLKLpfrdu/7zBSOid4vUEvS5iszjN7ypmffjtYtURRvSE5Ofkl2ZLbb7V/ZbLb35XouUWCSmDxqVdqsSpf/PrOSPjKZldQsNNMZwmRmLJkZFvw4HI4xlNIbExMT+xUXF5cTRXE8IaQdFn90uVyY8VL0lnNY5y1pMTwmb0ANJrEqbf50YRFPSml7URSHJCQk7BNF8XlCyB6sAo7Z2SmlYwkhPc2QudmqtFmVLi/wueAMsYo+MpmZ7wxhMjOezAwLfniex+rdJwVBwH9LzeFwvCWK4kUAcJOc+jozM7OPKIqTOY67ODc3F6thGz41u1VpC0YXFl1F/yxvraS7AQCrtx8VRXGE0fMT+VzRBdRHs9PGZEZNp49MZkxmGnyDazaEWfXRsOAHw6ABYLDH47l+69atO30A0CxKaXdBELK8eThIVlZWBd804JpJVaeBrEpbMLp4nv8IANoIgtAWwWlGRkYNm812FivU68RizYe1Km1Wpct7JRLwDDG7PjKZme8MYTIznsyMDH6aEEKewWsSjuOm+9bjwqrSAPCcIAi/av6Wi8GAWEHZirSFosvhcKyhlD4tCMJvMWCx5lNYlTar0uUFP0H3mZn1kcnMfGcIk5nxZGZY8OM9vG4jhGBCw41Y5DIvLw+jh/D66w9CyESzOMoGehPb7XZL0mZVuqysj0xmmmNl3QdkMtOdxZpPwGSmOUujGtAQ4MfhcFzkraMjESOHs/s4LWJmy8qEEMzwXAMAHieEdDWJo6wlaWMyM58+MpkxmUX1ttD4Yavqo1Xp8r6PLfM+izv44Xn+CwAYSCnNcLlcW33Tk2NGYADYarPZVns8HnR0xqJuh7DCshkcZa1Km1Xpws1tVdqsSheTGTsbNcZkUQ3H9pl59DGu4Mdbz4oHgF2U0sFe8CMpH8/znwBAN0EQMuQILsztk5qaSs2QEdiqtFmVLq/OoWXRcvrIZGa+M4TJjMksKhSm8cNW1Me4gR+e538BgMqCIPTgef59QsgOp9M5DgBsPM+3AIApqampl2DpCrPVfbIqbValywt8LKmPTGbmO0OYzJjMNMYuUQ1nVX2MC/hxOBwjKKUDBEG41OtI+johpJYgCJhz44JmNuBjVdqsSpf3HtuS+shkVnKUmOkMYTJjMosKqWj8sJX1MS7gp1mzZo1ycnJ2yHJyOBwOSumPoigOdrvdCzWWX0yHsyptVqULlcOqtFmVLiazmB5pmk1mVX20Kl1W3mdIW0zBD3rBnzp1avnevXsLvDsKa3Fh6HoFSukkSukGb+FL09To8gFwlqSNyUwqxGoqfWQyYzLTDLFoMJBV9dGqdHnfyZZ8n/mqc8zAT0ZGRheO4xDgzKSUfu52u895wZdUjsLhcNxOKZ3OcVzH3NxcwUwvHKvSZlW6UN+sSptV6WIyY2ejBjhMsyHYPjOnPsYL/LTlOG4FAPxKCPnj3Llzs7dv334WHZy9ZSowwutNAOhPCLnU6XTu1UxTdR4oIyPDkrRZlS7vi5TJjO0znU8GZcOzfWa+c5/JzHwy89+NMbP82O32zgDwAsdxGzGnD6X0j6Kioo8QAMkOic2aNbN7PJ7hHo9nvJzNWdnxEd9eVqXNqnShtliVNqvSxWTGzsb4nvIXzs72mTn1MS6WH4fDMZJSihFdT/E8/ywhpJUoin/JAEheVHp6ejmvRchIuh5yLValzap0ea9ZLamPTGYAZjtDmMyYzIz0srOyPsYE/PA8fx8h5LjH4znndrsxeRykpaWV37179xk8nJKSkrBERUu0ABUUFMzBvxtJAUKtxaq0WZUulKVVabMqXUxm7Gw00vuA7TNz6mMoHdLl2ovn+Z8BIJ0QsoFS2gcA5gPAKEEQDsuLwWzNJ0+eRADUi1L6mcvl+tBIyh5sLValzap0eV+iltRHJjPznSFMZkxmRnrPWVkfw/FZc/CTkZHRleO4iYIgdPU6ltbkOO5vQsgmm832SHZ29n4EPpi5GQuYejyeUR6P51O327073GLj/btVabMqXV79s6Q+MpmZ7wxhMmMyi/c7zHd+K+ujEj5rDn7sdnsvQsic1NTUpghwZABks9l+p5RuEQThTvybmbKuyoy0Km1WpQvlZlXarEoXkxk7G5W8uGLVh+0zc+qjEv3QDPzwPH8tpTQFK7BTSp8TRXGdy+XC0HWp8TxfAwByAeB5QRCmKVmcUfpYlTar0uXVN0vqI5OZ+c4QJjMmM6O8y6x8NkbKY03AD8/z31FKGxBCjgFAa8zlQyktIIQsEwRhjlyVnef5FwAgESO+Il1ovPpblTar0uXd3JbURyYz6SPKVGcIkxmTWbzeXYHmtbI+RsrnqMGP3W4fwnHcXU6ns5vXZP0oIeRxSulXhJAqlNKFLpdrJv7mcDjeAoAkp9P5gG9250gXHav+VqXNqnR59c+S+shkZr4zhMmMySxW7yol81hZH5XQ798navCDOXsAoKYgCA9jSQqHw9ECAGYgIPJ4PDcCQEcAaAoAWLD0LpvN1j0nJ2ezmsXG+hmr0mZVurxWH0vqI5OZ+c4QJjMms1i/s0LNZ2V9VMPnqMGPw+G4hlI6TBTF29xu9yGvb89iQkin5ORk0ePxJBcWFj5ACNkFACsFQUC/H1M0q9JmVbq81kVL6iOTmfnOECYzJjMjveisrI9q+Bw1+MGEhQkJCc3cbvc6XEBGRkY7juN+SE5ObrVp06ZjWLAUAE46nc4f1Swwns9YlTar0oW6YlXarEoXkxk7G+N5xvvPzfaZOfVRjQ5FDX78J3U4HN0ppZ8IgtDE4XA84K3U3jo3N3eTmgUa6Rmr0mZVuryWIEvqI5OZkU4GZWthMlPGJyP1YjIzkjS0XYvm4Ifn+U6EkDGU0n8A4CVRFC+SrULaLj32o1mVNqvS5fUBsqQ+MpnFfv9HOyOTWbQcjP3zTGax53msZtQc/DgcjlaU0vUAcEoUxT5WAT5eK4IlaWMyi9V2024eJjPteBmrkZjMYsVp7eZhMtOOl0YbSXPw06pVqwpnz56dQQh5yel0Oo1GcDTrsSptVqULZW1V2qxKF5NZNCdU/J61qj5alS4r7zOlu0Bz8IMTY82u7OzsQqWLMFM/q9JmVbqsrI9MZmY6OUrWymTGZGYkDlhZH8PxWRfwE25S9jvjAOMA4wDjAOMA4wDjQLw4wMBPvDjP5mUcYBxgHGAcYBxgHIgLBxj4iQvb2aSMA4wDjAOMA4wDjAPx4gADP/HiPJuXcYBxgHGAcYBxgHEgLhxg4CcubGeTMg4wDjAOMA4wDjAOxIsDDPzEi/NsXsYBxgHGAcYBxgHGgbhwgIGfuLCdTco4wDighgM8z28HgEY+zxYRQvZRSr8hhDzndDpPKRk3IyMjixDS2OVy/aKkP+vDOMA4YC0OMPBjLXkyahgHLM0BBD+U0rmJiYmTkdDCwsIKHMd1AIAJALAjISGhr5IcYzzPuwDgU0EQnrc0wxhxjAOMAwE5wMAPUwzGAcYB03DAC37ed7lcL/kuOiMjox3HcasppQ+6XK4Z4Qjied4NAHMY+AnHKfY744A1OcDAjzXlyqhiHLAkB4KBHySW5/lFhBDR6XT2sdvtNxBCngCAFgBAAWAdAIwUBGGVw+FYQCnt7WXQDkEQ0uvVq5eSmpr6KqX0FgAoBwBrRFF8xEq1CS2pEIwoxgGVHGDgRyXj2GOMA4wDsedAGPAzHQAQvPQDgOUAMJzjuF9EUaxJCHmLUvr/9u4ntI4qiuP478wsQiPdlOIiKzczk0dQCyIulEIFoVC1CxdCcaELN8UuBFEXLgtWN4V0UYVKcaeIoCC0lO6SUhAsCArOnUmJSALSpcRqJnNvGU3kEaPeRWN4N9/1OzNzz+c8Hj/m35t2zh2Zm5s71HXdN5I+996/17btnbIsPx7+fULS62Z2J4TwsqQzfd+PlpaWfvr/O+WICCCwmwKEn93UZd8IIHBfBf4t/FRVdTaE8FYI4XFJTzRN8+HWwYuieMXMLjnn8s2zRH9d9pqdnX3Ie3/be/9w27bfb21TluVNM1uo6/rN+9oEO0MAgT0XIPzs+QhYAAIIxAr8x5mfeUmnnHOHNwPNKUkjSYWkI5IakuiyAAACmElEQVSmnHN//OaN3/NTFMUJM/tK0tq2dUxJuuqcey52fdQhgMBkCBB+JmNOrBIBBP4MLcPTXn+74Xkz0CxK+t3MhjNAVyR9GUK4EUL41sxmzeyDncJPVVUnQwhfZFn2SNd1d8eh8zy/65xbAR8BBNISIPykNU+6QSBpgX8KP2VZPjrc1Gxmr3rvj2dZNlXX9fNjl7DelfS2cy4bboAef9R9NBoVfd+7EMIzTdNc39qmKIqPJC02TXM5aVSaQ2AfChB+9uHQaRmBSRXY/p6fruumzexJSeckLc3MzDy9srIyn2XZib7vX8zz/Gfv/bNm9v7wFNf6+vqB5eXl38qyvCXpBzN7o67r1aIoPjOzx8zs9MbGRpvn+WlJr0l6yjn39aR6sW4EENhZgPDDNwMBBCZGYIc3PP8SQvhR0idra2vnV1dXfy3L8rCkS5KOSeqHy15Zll0MIXwq6ahzbqGqqpdCCBeGz51zD1ZV9cDw5JeZvSDpoKTvvPfvtG17bWJwWCgCCEQLEH6iqShEAAEEEEAAgRQECD8pTJEeEEAAAQQQQCBagPATTUUhAggggAACCKQgQPhJYYr0gAACCCCAAALRAoSfaCoKEUAAAQQQQCAFAcJPClOkBwQQQAABBBCIFiD8RFNRiAACCCCAAAIpCBB+UpgiPSCAAAIIIIBAtADhJ5qKQgQQQAABBBBIQYDwk8IU6QEBBBBAAAEEogUIP9FUFCKAAAIIIIBACgKEnxSmSA8IIIAAAgggEC1A+ImmohABBBBAAAEEUhAg/KQwRXpAAAEEEEAAgWgBwk80FYUIIIAAAgggkIIA4SeFKdIDAggggAACCEQLEH6iqShEAAEEEEAAgRQECD8pTJEeEEAAAQQQQCBa4B4JxGot8B3IgwAAAABJRU5ErkJggg==" width="638.888905813665">



```python
# Use Pandas to calcualte the summary statistics for the precipitation data
precip.describe()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>123.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.055854</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.116640</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.060000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>0.560000</td>
    </tr>
  </tbody>
</table>
</div>



### station analysis


```python
# How many stations are available in this dataset?
stations_df['name'].count()
```




    9




```python
# What are the most active stations?
# List the stations and the counts in descending order.
merge_data.station.value_counts()
```




    USC00519281    2772
    USC00519397    2724
    USC00513117    2709
    USC00519523    2669
    USC00516128    2612
    USC00514830    2202
    USC00511918    1979
    USC00517948    1372
    USC00518838     511
    Name: station, dtype: int64




```python
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
max_temp = merge_data[merge_data['station']=='USC00519281']
max_temp = max_temp['tobs'].max()
min_temp = merge_data[merge_data['station']=='USC00519281']
min_temp = min_temp['tobs'].min()
avg_temp = merge_data[merge_data['station']=='USC00519281']
avg_temp = avg_temp['tobs'].mean()

print('the max temp is {}, the min temp is {}, the average temp is {} for station USC00519281'.format(max_temp, min_temp, avg_temp))

```

    the max temp is 85.0, the min temp is 54.0, the average temp is 71.66378066378067 for station USC00519281
    


```python
most_obs = merge_data.groupby('station').count().max()
most_obs
```




    date         2772
    prcp         2772
    tobs         2772
    name         2772
    latitude     2772
    longitude    2772
    elevation    2772
    dtype: int64




```python
#12months data
temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2017-07-27').order_by(Measurement.date).all()
temp_df = pd.DataFrame(temps, columns=['Station', 'date', 'temp'])
temp_df.set_index('Station', inplace=True)
temp_df.sample(20)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>temp</th>
    </tr>
    <tr>
      <th>Station</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>USC00514830</th>
      <td>2017-07-28</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-07-31</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>USC00519281</th>
      <td>2017-07-29</td>
      <td>82.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-02</td>
      <td>73.0</td>
    </tr>
    <tr>
      <th>USC00513117</th>
      <td>2017-07-29</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-13</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-15</td>
      <td>78.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-18</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>USC00514830</th>
      <td>2017-08-03</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00516128</th>
      <td>2017-08-17</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>USC00516128</th>
      <td>2017-08-18</td>
      <td>76.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-14</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>USC00516128</th>
      <td>2017-08-11</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>USC00514830</th>
      <td>2017-08-09</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-07-28</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00516128</th>
      <td>2017-08-06</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>USC00519397</th>
      <td>2017-08-03</td>
      <td>79.0</td>
    </tr>
    <tr>
      <th>USC00519281</th>
      <td>2017-07-28</td>
      <td>81.0</td>
    </tr>
    <tr>
      <th>USC00519523</th>
      <td>2017-08-22</td>
      <td>82.0</td>
    </tr>
    <tr>
      <th>USC00519281</th>
      <td>2017-07-31</td>
      <td>76.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
hist_plot = temp_df['temp'].hist(bins=12)
hist_plot.set_title('Temperature Observations')
hist_plot.set_ylabel('Frequency')
plt.show()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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" width="639.2593044181615">


### temperature analysis


```python
start_date = '2017-06-15'
end_date = '2017-06-27'

# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
print(calc_temps(start_date, end_date))
```

    [(71.0, 77.07407407407408, 82.0)]
    


```python
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
hist_start_date = dt.date(2018, 7, 23) - dt.timedelta(days=365)
hist_end_date = dt.date(2018, 8, 5) - dt.timedelta(days=365)
trip_temps = calc_temps(hist_start_date, hist_end_date)
trip_temps
```




    [(72.0, 78.88157894736842, 84.0)]




```python
fig, ax = plt.subplots()
x = range(len(trip_temps))
ax.boxplot(trip_temps, patch_artist=True)
ax.set_title('Trip Avg Temp')
ax.set_ylabel("Temp(F)")
ax.set_xlabel("Trip")
fig.tight_layout()
plt.show()
```


    <IPython.core.display.Javascript object>



<img src="data:image/png;base64,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" width="639.2593044181615">



```python
# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
merge_data['date'] = pd.to_datetime(merge_data['date'], format = '%Y-%m-%d')
trip_dates = (merge_data['date'] >= hist_start_date) & (merge_data['date'] <= hist_end_date)
trip_weather = merge_data.loc[trip_dates].dropna()
trip_weather = trip_weather.groupby('station')['prcp'].sum().reset_index()
result = pd.concat([trip_weather, stations_df], axis=1, join='inner')
result = result.sort_values('prcp', ascending=False)
result
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>station</th>
      <th>prcp</th>
      <th>id</th>
      <th>station</th>
      <th>name</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>elevation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>USC00516128</td>
      <td>3.55</td>
      <td>3</td>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.52130</td>
      <td>-157.83740</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00514830</td>
      <td>1.78</td>
      <td>2</td>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519281</td>
      <td>1.43</td>
      <td>5</td>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.49920</td>
      <td>-158.01110</td>
      <td>306.6</td>
    </tr>
    <tr>
      <th>0</th>
      <td>USC00513117</td>
      <td>0.92</td>
      <td>1</td>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00519397</td>
      <td>0.09</td>
      <td>6</td>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>21.33556</td>
      <td>-157.71139</td>
      <td>19.5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00519523</td>
      <td>0.05</td>
      <td>7</td>
      <td>USC00519281</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00517948</td>
      <td>0.01</td>
      <td>4</td>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.39340</td>
      <td>-157.97510</td>
      <td>11.9</td>
    </tr>
  </tbody>
</table>
</div>



### climate app


```python
from flask import Flask, jsonify
app = Flask(__name__)

#Query for the dates and temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def temp_obs_year():
    temps = engine.execute("""SELECT date, round(avg(tobs), 2) as temp
        FROM measurement
        WHERE strftime('%Y', date) = '2017'
        GROUP BY date
        ORDER BY date
    """).fetchall( )
    temp_key_values = {k:v for k,v in temps}
    return jsonify(temp_key_values)
```


```python
#return json list of the stations
@app.route("/api/v1.0/stations")
def stations():
    station_list = {}
    station_list['data'] = []
    for row in session.query(station):
        station_list['data'].append(
            {"station": row.station,
            "name": row.name})
    return jsonify(station_list)
```


```python
# Return a JSON list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    prev_temps = {}
    prev_temps['data'] = []
    temps = engine.execute("""SELECT date, tobs
            FROM measurement
            WHERE strftime('%Y', date) = '2017'
            GROUP BY date
            ORDER BY date
        """).fetchall()
    for row in temps:
        prev_temps['data'].append(
        {'date': row.date,
        'temp': row.tobs})
    return jsonify(prev_temps)
    
```


```python
# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive

start = '2017-01-01'
end= '2017-01-07'

@app.route("/api/v1.0/<start>/<end>/")
def start_end_weather(start, end):
    weather_rows = engine.execute("""SELECT  
        round(avg(tobs), 2) as avg_temp,
        round(min(tobs), 2) as min_temp,
        round(max(tobs), 2) as max_temp
        FROM measurement
        WHERE date BETWEEN '{}' AND '{}'
    """.format(start, end)).fetchall()
    return jsonify({"data": [dict(x) for x in weather_rows]})

```


```python
# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.
#all dates greater than and equal to the start date

@app.route("/api/v1.0/<start>/")
def start_weather(start):
    trip_weather = engine.execute("""SELECT  
        round(avg(tobs), 2) as avg_temp,
        round(min(tobs), 2) as min_temp,
        round(max(tobs), 2) as max_temp
        FROM measurement
        WHERE date >= '{}'
        """.format(start)).fetchall()
    return jsonify({"data": [dict(x) for x in trip_weather]})

```
