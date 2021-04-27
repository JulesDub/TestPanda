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
    #Lecture du premier CSV
    data = pd.read_csv('import_colonies_fev2021.csv', usecols=['secteur_nom_fr', 'longitude', 'latitude'], sep=';', encoding="utf8")
    new_data = data.replace(["'", '		'], [" ", ''], regex=True)#removing " ' " char and multiple spaces unwanted which create bug on json object
    new_data = new_data.dropna()#for cleaning empty data in csv
    for x in new_data.index:
        if new_data.loc[x, "longitude"] > 180:#for cleaning wrong lng in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, "longitude"] < -180:
            new_data.drop(x, inplace=True)
        if new_data.loc[x, "latitude"] > 90:#for cleaning wronf lat in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, "latitude"] < -90:
            new_data.drop(x, inplace=True)
    dfdata = pd.DataFrame(new_data, columns=['secteur_nom_fr', 'latitude', 'longitude'])

    #Lecture du second CSV
    datab = pd.read_csv('Export_Rinbio.csv', usecols=['LIEU_LIBELLE', 'LONGITUDE', 'LATITUDE'], encoding="utf8")
    new_datab = datab.replace(["'", '		'], [" ", ''], regex=True)  # removing " ' " char and multiple spaces unwanted which create bug on json object
    new_datab = new_datab.dropna()  # for cleaning empty data in csv
    for x in new_datab.index:
        if new_datab.loc[x, "LONGITUDE"] > 180:  # for cleaning wrong lng in csv
            new_datab.drop(x, inplace=True)
        elif new_datab.loc[x, "LONGITUDE"] < -180:
            new_datab.drop(x, inplace=True)
        if new_datab.loc[x, "LATITUDE"] > 90:  # for cleaning wrong lat in csv
            new_datab.drop(x, inplace=True)
        elif new_datab.loc[x, "LATITUDE"] < -90:
            new_datab.drop(x, inplace=True)
    dfdatab = pd.DataFrame(new_datab, columns=['LIEU_LIBELLE', 'LATITUDE', 'LONGITUDE'])
    dataf = dfdata.values.tolist()
    databf = dfdatab.values.tolist()
    dataID = [[len(dataf), len(databf)]]#Created a list to get the length of both CSV
    dataf = dataf + databf + dataID #Created the final list which will be send to python
    return render_template('leaflet.html', data=json.dumps(dataf))

if __name__ == '__main__':
    app.run(debug=True)
