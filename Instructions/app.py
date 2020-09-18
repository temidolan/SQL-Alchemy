from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

measurement=Base.classes.measurement
station=Base.classes.station

app = Flask(__name__)

session= Session(engine)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<startdate><br/>"
        f"/api/v1.0/<startdate>/<enddate><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():


    precipitation_date=session.query(measurement.date).order_by(measurement.date.desc()).first()
    prev_year = dt.date(2017,8,23) - dt.timedelta(days= 365)

    precipitation_dt= session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >=prev_year).all()

    return jsonify(dict(precipitation_dt))

@app.route("/api/v1.0/stations")
def stations():
    stationz = session.query(measurement.station).distinct().count()
    active_stations=session.query(measurement.station,func.count(measurement.station)).\
                group_by(measurement.station).\
                order_by(func.count(measurement.station)).all()

    return jsonify(dict(active_stations))


@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days= 365)
    tobx = (session.query(measurement.date, measurement.tobs, measurement.station).filter(measurement.date > prev_year)
                      .order_by(measurement.date).all())
    tobs_list = []
    for i in tobx:
        tobs_temp = {i.date: i.tobs, "Station": i.station}
        tobs_list.append(tobs_temp)
    return jsonify(tobs_list)

    # temp_obs =[]
    # i = 0
    # while len(active_station) > i:
    #       temp_obs.append(session.query(measurement.station, func.count(measurement.tobs)).filter(measurement.station == active_station[i][0]).order_by(func.count(measurement.tobs)).all())
    # i+=1
    # print(temp_obs[0])

    # return jsonify(temp_obs)

@app.route("/api/v1.0/<startdate>")
def start(startdate):
    sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    start_results =  (session.query(*sel).filter(measurement.date >= startdate)
                       .group_by(measurement.date).all())
    begin_dates = []                       
    for i in start_results:
        date = {}
        date["Date"] = i[0]
        date["Min Temp"] = i[1]
        date["Avg Temp"] = i[2]
        date["Max Temp"] = i[3]
        begin_dates.append(date)
    return jsonify(begin_dates)



@app.route("/api/v1.0/<startdate>/<enddate>")
def startend(startdate, enddate):
    sel2= [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    duration_results =  (session.query(*sel2).filter(measurement.date >= startdate)
                       .filter(measurement.date<= enddate).group_by(measurement.date).all())
    startend_dates = []                       
    for i in duration_results:
        date = {}
        date["Date"] = i[0]
        date["Min Temp"] = i[1]
        date["Avg Temp"] = i[2]
        date["Max Temp"] = i[3]
        startend_dates.append(date)
    return jsonify(startend_dates)
if __name__ == "__main__":
    app.run(debug=True)
