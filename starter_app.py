from flask import Flask, jsonify, render_template
import json
import requests
from flask import request
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def temp_obs_year():
    temps = engine.execute("""SELECT date, round(avg(tobs), 2) as temp
        FROM measurement
        WHERE strftime('%Y', date) = '2017'
        GROUP BY date
        ORDER BY date
    """).fetchall()
    temp_key_values = {k:v for k,v in temps}
    return jsonify(temp_key_values)

@app.route("/api/v1.0/stations")
def stations():
    station_list = {}
    station_list['data'] = []
    for row in session.query(station):
        station_list['data'].append(
            {"station": row.station,
            "name": row.name}
        )
    return jsonify(station_list)

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