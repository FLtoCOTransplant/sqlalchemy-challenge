  
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

    # Convert the results to a dictionary and print JSON object
    return jsonify(precip_data)

    session.close()
if __name__ == "__main__":
    app.run(debug=True)
