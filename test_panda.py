import pandas as pd
import csv
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def map_func():
    return render_template('home.html')


@app.route('/leaflet')
def leaflet():
    namef = pd.read_csv('import_colonies_fev2021_OG.csv', usecols=['secteur_nom_fr'], sep=';', encoding="utf8")
    longf = pd.read_csv('import_colonies_fev2021_OG.csv', usecols=['longitude'], sep=';')
    latf = pd.read_csv('import_colonies_fev2021_OG.csv', usecols=['latitude'], sep=';')

    new_name = namef.dropna()
    new_long = longf.dropna()
    new_lat = latf.dropna()

    for x in new_long.index:
        if new_long.loc[x, "longitude"] > 180:
            new_long.drop(x, inplace=True)

    for x in new_lat.index:
        if new_lat.loc[x, "latitude"] > 90:
            new_lat.drop(x, inplace=True)

    dfname = pd.DataFrame(new_name, columns=['secteur_nom_fr'])
    dfx = pd.DataFrame(new_long, columns=['longitude'])
    dfy = pd.DataFrame(new_lat, columns=['latitude'])

    name = dfname.values.tolist()
    long = dfx.values.tolist()
    lat = dfy.values.tolist()
    return render_template('leaflet.html', Long=json.dumps(long), Lat=json.dumps(lat), ID=json.dumps(name))
    """Id = pd.read_csv('ville.csv', usecols=['Name'],sep=';',encoding='utf8')
	Long1 = pd.read_csv('ville.csv', usecols=['Long'],sep=';') 
	Lat1 = pd.read_csv('ville.csv', usecols=['Lat'],sep=';') 

	dfid= pd.DataFrame(Id,columns=['Name'])
	dfx= pd.DataFrame(Long1,columns=['Long'])
	dfy= pd.DataFrame(Lat1,columns=['Lat'])

	ID = dfid.values.tolist()
	Long = dfx.values.tolist()
	Lat = dfy.values.tolist()
	return render_template('leaflet.html', ID=json.dumps(ID), Long=json.dumps(Long),Lat=json.dumps(Lat))"""


if __name__ == '__main__':
    app.run(debug=True)
