from flask import Flask, render_template
import pandas as pd
import json

app = Flask("Website")


@app.route("/")
def home():
    df=pd.read_csv("data_small/stations.txt",skiprows=17)
    select=df[['STAID', 'STANAME                                 ']]
    tables=select.to_html(index=False)
    return render_template("home.html",data=tables)



@app.route("/api/v1/<station>/<date>")
def data(station, date):
    df = pd.read_csv(r"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20,parse_dates=['    DATE'])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    return {"station": station, "date": date, "temperature": temperature}

@app.route("/api/v1/<station>")
def data_station(station):
    df = pd.read_csv(r"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=['    DATE'])
    result=df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def year(station,year):
    df = pd.read_csv(r"data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20)
    df['    DATE']=df['    DATE'].astype(str)# it converts the date column to string
    result=df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return  result



"""App.route is like a domain_name/home to access the page dynamically"""

app.run(debug=True)
