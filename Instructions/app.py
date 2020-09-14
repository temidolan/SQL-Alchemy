%matplotlib inline
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
    return ( """<html>
         <a href = f"/api/v1.0/precipitation"
         <a href =f"/api/v1.0/stations"
         <a href =f"/api/v1.0/tobs"
         <a href =f"/api/v1.0/<start> "
         <a href =f"/api/v1.0/<start>/<end>" </a></html>"""
    )

