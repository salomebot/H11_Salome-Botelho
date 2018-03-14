#Climate app
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func
import numpy as np
import pandas as pd
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
print("Connected to DB")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print("Reflected tables")

# Save reference to the table
Measurement = Base.classes.clean_hawaii_measurements
Station = Base.classes.clean_hawaii_stations

# Create our session (link) from Python to the DB
session = Session(engine)

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
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/>\
            /api/v1.0/tobs<br/>\
            /api/v1.0/start/end")


@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return the json representation of your dictionary.
    """
    # Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >"2017-01-01", Measurement.date < "2017-12-31").\
    order_by(Measurement.date).all()

    data ={record.date: record.prcp  for record in  results}
    return jsonify(data)

# Return a json list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    """ Return a json list of stations from the dataset.
    """
    stations_name = session.query(Station.name).all()
    #all_stations_names = [record for record in stations_name]
    #return jsonify( stations_name)
    return '<br>'.join(str(x) for x in   stations_name)

"""Return a json list of Temperature Observations (tobs) for the previous year
"""
@app.route("/api/v1.0/tobs")
def tobs():
    """ Return a json list of Temperature Observations (tobs)
    """
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.date >"2017-01-01", Measurement.date < "2017-12-31").\
    order_by(Measurement.date).all()
    return '<br>'.join(str(x) for x in tobs)
    #tobs_last_yr= list(np.ravel(tobs))
    #return jsonify(tobs_last_yr)

"""Return a json list of the minimum temperature, the average temperature,
 and the max temperature for a given start or start-end range.
"""
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def daily_normals(start, end):
    normals=[Measurement.station,
         Station.name,
         func.min(Measurement.tobs),
         func.max(Measurement.tobs),
         func.avg(Measurement.tobs)]

    daily_normal=session.query(*normals).filter(Measurement.station==Station.station).\
filter(Measurement.date >= start).\
group_by(Measurement.station).all()

    return '<br>'.join(str(x) for x in daily_normal)
"""ask about start and end??
"""
if __name__ == "__main__":
    app.run(debug=True)
