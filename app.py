  
from flask import Flask, jsonify
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect the existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask initiation
app = Flask(__name__)

# Flask routes

@app.route("/")
def Home():
    return(
        f"Welcome to your historical Hawaii Weather homepage"
        f"You can browse:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Link from python to the sqlite db
    session = Session(engine)

    """Return all precipitation data"""
    # Query for all precipitation data
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    session.close()

     # List of tuples into list
    precip_all = list(np.ravel(precip_data))
    
    # List to Dictionary
    precip_all = {precip_all[i]: precip_all[i + 1] for i in range(0, len(precip_all), 2)}

    # Convert the results to a dictionary and print JSON object
    return jsonify(precip_all)

@app.route("/api/v1.0/stations")
def stations():
    # Link from python to the sqlite db
    session = Session(engine)

    """Return all Stations"""
    # Query all Stations
    stations = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    # List of tuples into list
    stations = list(np.ravel(stations))

    # Print JSON object
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Link from python to the sqlite db
    session = Session(engine)

    """Return all TOBs"""
    # Query all tobs

    station_obs = session.query(Measurement.date,  Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').\
                    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(station_obs))

    # Convert the list to Dictionary
    tobs = {tobs[i]: tobs[i + 1] for i in range(0, len(tobs), 2)} 

    return jsonify(tobs)

@app.route("/api/v1.0/<start_date>")
def data_start_date(start_date):
    # Link from python to the sqlite db
    session = Session(engine)

    """Return min, avg and max tobs for the start date of the vacation"""
    # Query all tobs

    vac_temp_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= '2012-02-28').all()

    session.close()
    
    # Dictionary from the row data and append to a list of vacaction temp obs
    vac_temp_s_tobs = []
    for min, avg, max in vac_temp_start:
        vac_temp_s_dict = {}
        vac_temp_s_dict["min_temp"] = min
        vac_temp_s_dict["avg_temp"] = avg
        vac_temp_s_dict["max_temp"] = max
        vac_temp_s_tobs.append(vac_temp_s_dict)

    return jsonify(vac_temp_s_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def data_start_end_date(start_date, end_date):
    # Link from python to the sqlite db
    session = Session(engine)

    """Return min, avg and max tobs for the end date of the vacation"""
    # Query all tobs

    vac_temp_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= '2012-03-05').all()

    session.close()
    
    # Dictionary from the row data and append to a list of vacaction temp obs
    vac_temp_e_tobs = []
    for min, avg, max in results:
        vac_temp_e_dict = {}
        vac_temp_e_dict["min_temp"] = min
        vac_temp_e_dict["avg_temp"] = avg
        vac_temp_e_dict["max_temp"] = max
        vac_temp_e_tobs.append(vac_temp_e_dict) 
    
    return jsonify(vac_temp_e_tobs)

if __name__ == "__main__":
    app.run(debug=True)
