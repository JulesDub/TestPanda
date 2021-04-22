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
    Id = pd.read_csv('import_colonies_fev2021.csv', usecols=['secteur_nom_fr'], sep=';', encoding="utf8")
    Long1 = pd.read_csv('import_colonies_fev2021.csv', usecols=['longitude'], sep=';')
    Lat1 = pd.read_csv('import_colonies_fev2021.csv', usecols=['latitude'], sep=';')

    dfid = pd.DataFrame(Id, columns=['secteur_nom_fr'])
    dfx = pd.DataFrame(Long1, columns=['longitude'])
    dfy = pd.DataFrame(Lat1, columns=['latitude'])

    ID = dfid.values.tolist()
    Long = dfx.values.tolist()
    Lat = dfy.values.tolist()
    return render_template('leaflet.html', Long=json.dumps(Long), Lat=json.dumps(Lat), ID=json.dumps(ID))
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



