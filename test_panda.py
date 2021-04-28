import pandas as pd
import csv
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def map_func():
    return render_template('home.html')

def csv_cleaner(path_csv, nom, lng, lat, sep):
    data = pd.read_csv(path_csv, usecols=[nom, lng, lat], sep=sep, encoding="utf8")
    new_data = data.replace(["'", '		'], [" ", ''], regex=True)  # removing " ' " char and multiple spaces unwanted which create bug on json object
    new_data = new_data.dropna()  # for cleaning empty data in csv
    for x in new_data.index:
        if new_data.loc[x, lng] > 180:  # for cleaning wrong lng in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, lng] < -180:
            new_data.drop(x, inplace=True)
        if new_data.loc[x, lat] > 90:  # for cleaning wrong lat in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, lat] < -90:
            new_data.drop(x, inplace=True)
    data_frame_f = pd.DataFrame(new_data, columns=[nom, lat, lng])
    data_list_f = data_frame_f.values.tolist()
    return data_list_f

@app.route('/leaflet')
def leaflet():
    data_list_a = csv_cleaner("CSV_file/import_colonies_fev2021.csv", "secteur_nom_fr", "longitude", "latitude", ";")
    data_list_b = csv_cleaner("CSV_file/Export_Rinbio.csv", "LIEU_LIBELLE", "LONGITUDE", "LATITUDE", ",")
    data_length = [[len(data_list_a), len(data_list_b)]]#Created a list to get the length of both CSV
    all_data = data_list_a + data_list_b + data_length #Created the final list which will be send to python
    return render_template('leaflet.html', data=json.dumps(all_data))

if __name__ == '__main__':
    app.run(debug=True)


