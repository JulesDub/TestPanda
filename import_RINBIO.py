import pandas as pd
import csv
import json
import psycopg2


#Connection à la base SIMM_LIEUX de PRODUCTION
conn_simm_lieux = psycopg2.connect(host='vpostgres10.ifremer.fr',database="simm_lieux",user='simm_lieux_user',password='Motocyclette bionique et menestrel par ordre alphabetique',port= '5432')
cursor_simm_lieux = conn_simm_lieux.cursor();

# TODO Récupérer ces informations depuis la fiche dispositif (ExtractWord.py)
nom_dipositif="Réseau INtégrateurs BIOlogiques (RINBIO)"
programmes="Contaminants/SP01 Contaminants chimiques dans les organismes marins;Contaminants/SP02 Contaminants chimiques dans le milieu;Contaminants/SP03 Effets des contaminants chez les organismes marins"
parametres = """CONC-B1 - Concentration dans le biote;CONC-B2 - Concentration dans le biote - muscle;CONC-MOL - Concentration dans les mollusques bivalves;CONC-S1 - Concentration dans les sédiments;ECOTOX-Spp2 - Stabilité de la membrane lysosomale (LMS);OTH - Autres"""
critère_BEE="""D8C1 - Contaminants dans l'environnement"""
indicateur_BEE="Concentration en HAP chez les bivalves;Concentration en PCB chez les bivalves;Concentration en pesticides chez les bivalves;Concentration en dioxines - PCB-DL chez les bivalves;Concentration en métaux chez les bivalves;Concentration en organoétains chez les bivalves"
OE="""D08-OE07"""
indicateurs_OE="""D08-OE07-ind1;D08-OE07-ind2;D08-OE07-ind3"""
Bancarisation="""Quadrige"""

# Fonction pour importer en base
def import_into_database(file="import_colonies_fev2021.csv"):
    data_nom = pd.read_csv(file, usecols=['secteur_nom_fr'], sep=';')
    data_longitude = pd.read_csv(file, usecols=['secteur_nom_fr'], sep=';')
    data_latitude = pd.read_csv(file, usecols=['secteur_nom_fr'], sep=';')
    print(data_nom.to_string())



def write_SQL(list_csv):
    for x in range(len(list_csv)):

        request_sql = f"""INSERT INTO LIEUX_SEXTANT    (LIEU_LIBELLE,
                        	                                                LIEU_POSITION_POINT,
                        	                                                LIEU_DISPOSITIF,
                        	                                                LIEU_PDS,
                        	                                                LIEU_CRITERES_BEE,
                        	                                                LIEU_INDICATEURS_BEE,
                        	                                                LIEU_OE,
                        	                                                LIEU_INDICATEURS_OE,
                        	                                                LIEU_PARAMETRES,
                        	                                                LIEU_BANCARISATION)
                        	                    VALUES ('%s','POINT({list_csv[x][2]} {list_csv[x][1]})','%s',
                        	                    '%s',
                        	                    '%s','%s',
                        	                    '%s','%s',
                        	                    '%s','%s')"""
        cursor_simm_lieux.execute(
            request_sql % (list_csv[x][0].replace("'", "''"), nom_dipositif.replace("'", "''"),
                           programmes.replace("'", "''"),
                           critère_BEE.replace("'", "''"), indicateur_BEE.replace("'", "''"),
                           OE.replace("'", "''"), indicateurs_OE.replace("'", "''"),
                           parametres.replace("'", "''"),Bancarisation.replace("'", "''")))




# Clean des longitude/latitude
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


# Fonction pour convertir CSV en JSON
def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)


# Process de l'import
data_list_a = csv_cleaner("CSV_file/Export_Rinbio.csv", "LIEU_LIBELLE", "LONGITUDE", "LATITUDE", ",")
write_SQL(data_list_a)
conn_simm_lieux.commit()
conn_simm_lieux.close()