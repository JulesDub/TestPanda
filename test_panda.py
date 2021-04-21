import pandas as pd
import csv
import json
from flask import Flask,render_template,url_for
from geopy.geocoders import Nominatim
app = Flask(__name__)

@app.route('/')
def map_func():
	return render_template('home.html')

@app.route('/leaflet')
def marseille():
	"""for i in range(1,100):
		GeoCode[i+1] = pd.read_csv('import_colonies_fev2021.csv', usecols=['secteur_nom_fr'],sep=';')
		GeoCode[i+2] = pd.read_csv('import_colonies_fev2021.csv', usecols=['longitude'],sep=';') 
		GeoCode[i+3] = pd.read_csv('import_colonies_fev2021.csv', usecols=['latitude'],sep=';') 
	return render_template('leaflet.html', GeoCode=json.dumps(GeoCode))"""
	Id = pd.read_csv('ville.csv', usecols=['Name'],sep=';')
	Long1 = pd.read_csv('ville.csv', usecols=['Long'],sep=';') 
	Lat1 = pd.read_csv('ville.csv', usecols=['Lat'],sep=';') 

	dfid= pd.DataFrame(Id,columns=['Name'])
	dfx= pd.DataFrame(Long1,columns=['Long'])
	dfy= pd.DataFrame(Lat1,columns=['Lat'])

	ID = dfid.values.tolist()
	Long = dfx.values.tolist()
	Lat = dfy.values.tolist()
	return render_template('leaflet.html', ID=json.dumps(ID), Long=json.dumps(Long),Lat=json.dumps(Lat))


		   

	
if __name__ == '__main__':
    app.run(debug=True)    



				