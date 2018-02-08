# 
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime 
import time
import csv
##
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()
Measurement = Base.classes.Hawaii_m_table
Station = Base.classes.Hawaii_s_table
# Create a session
session = Session(engine)

#1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfer API! <br/>"
        f" Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(dict(session.query(Measurement.date,Measurement.prcp).filter(func.strftime("%Y", Measurement.date) == '2017').all()))

@app.route("/api/v1.0/stations")
def stations():
    query_stations=session.query(Station.station).all()
    return jsonify(query_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    query_tobs=session.query(Measurement.tobs).filter(func.strftime("%Y", Measurement.date) == '2017').all()
    return jsonify(query_tobs)

## Enter any start date in YYYY-MM-DD format below will display avg,max and min temperatures
@app.route('/api/v1.0/<start>')
def tobs_max_min_avg(start):
    start_date=("'%s'" %start)
    temp_list=[]
    query_tobs_avg=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >=start_date).all()
    query_tobs_max=session.query(func.max(Measurement.tobs)).filter(Measurement.date >=start_date).all()
    query_tobs_min=session.query(func.min(Measurement.tobs)).filter(Measurement.date >=start_date).all()
    temp_list=[query_tobs_avg,query_tobs_max,query_tobs_min]
    ## Open a file to save above values
    with open("output.csv","w",newline='') as fp:
        wr=csv.writer(fp,delimiter=',')
        wr.writerows(temp_list)
    with open("output.csv","r",newline='') as f:
        avg_reader=csv.reader(f)
        TAVG=[]
        for i in avg_reader:
            TAVG=TAVG+[i]
    my_temp=['TAVG','TMAX','TMIN']
    temp_display=dict(zip(my_temp,TAVG))
    return jsonify(temp_display)

@app.route('/api/v1.0/<start>/<end>')
def tobs_start_end(start,end):
    #start_date=("'%s'" %start)
    #end_date=("'%s'" %end)
    if (start != "" and end != ""):
        avg_result=session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
        min_result=session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
        max_result=session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).all()
        temp_list=[avg_result,max_result,min_result]

    ## Open a file to save above values
    with open("output.csv","w",newline='') as fp:
        wr=csv.writer(fp,delimiter=',')
        wr.writerows(temp_list)
    with open("output.csv","r",newline='') as f:
        avg_reader=csv.reader(f)
        TAVG=[]
        for i in avg_reader:
            TAVG=TAVG+[i]
    my_temp=['TAVG','TMAX','TMIN']
    temp_display=dict(zip(my_temp,TAVG))
    return jsonify(temp_display)


@app.route('/api/v1.0/<start>%20<end>/')
def start_end_range(start,end):
    #start_date=("'%s'" %start)
    #end_date=("'%s'" %end)
    avg_result=session.query(func.avg(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    #min_result=session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date<end_date).all()
    #max_result=session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date<end_date).all()
    temp_list=[avg_result]
## Open a file to save above values
    with open("output.csv","w",newline='') as fp:
        wr=csv.writer(fp,delimiter=',')
        wr.writerows(temp_list)
    with open("output.csv","r",newline='') as f:
        avg_reader=csv.reader(f)
        TAVG=[]
        for i in avg_reader:
            TAVG=TAVG+[i]
    my_temp=['TAVG','TMAX','TMIN']
    temp_display=dict(zip(my_temp,TAVG))
    return jsonify(temp_display)


    #canonicalized = realname.replace("","").lower()
    #for character in justice_league_members:
     #   search_term=character[realname].replace("","").lower()

      #  if search_term == canonicalized:
       #     return jsonify(character)

    #return jsonify({"error": f"Character with realname {realname} not found.404" })


if __name__=="__main__":
    app.run(debug=True)