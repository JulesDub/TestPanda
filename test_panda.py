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
    data = pd.read_csv('import_colonies_fev2021.csv', usecols=['secteur_nom_fr', 'longitude', 'latitude'], sep=';', encoding="utf8")
    new_data = data.dropna()

    for x in new_data.index:
        if new_data.loc[x, "longitude"] > 180:
            new_data.drop(x, inplace=True)
        if new_data.loc[x, "latitude"] > 90:
            new_data.drop(x, inplace=True)

    dfdata = pd.DataFrame(new_data, columns=['secteur_nom_fr', 'latitude', 'longitude'])

    dataf = dfdata.values.tolist()

    return render_template('leaflet.html', data=json.dumps(dataf))
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
