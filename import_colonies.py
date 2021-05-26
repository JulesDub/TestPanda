import pandas as pd
import csv
import json
import psycopg2



#Connection à la base SIMM_LIEUX de PRODUCTION
conn_simm_lieux = psycopg2.connect(host='vpostgres10.ifremer.fr',database="simm_lieux",user='simm_lieux_user',password='',port= '5432')
cursor_simm_lieux = conn_simm_lieux.cursor();


# TODO Récupérer ces informations depuis la fiche dispositif (ExtractWord.py)
nom_dispositif="""Suivi national des effectifs d’oiseaux marins nicheurs"""
#D1 = Biodiversité
programme="Oiseaux/SP02 Oiseaux marins nicheurs"
parametres="""ABU1-6 - Abondance (nombre)"""
critère_BEE="""D1C2 - Abondance des populations;D1C4 - Distribution spatiale des populations"""
indicateur_BEE="Abondance des couples d'oiseaux nicheurs (adaptation OSPAR B1)"
OE="""D01-OM-OE04;D01-OM-OE05;D01-OM-OE06"""
indicateurs_OE="""D01-OM-OE04-ind1;D01-OM-OE04-ind2;D01-OM-OE05-ind2;D01-OM-OE06-ind1;D01-OM-OE06-ind3"""
Bancarisation="""Bdd oiseaux OFB"""
Protocole = """http://oiseaux-marins.fr/IMG/pdf/GISOM-methodo_doc-entier.pdf"""


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
                        	                    '%s','%s',
                        	                    '%s',
                        	                    '%s','%s',
                        	                    '%s','%s')"""
        cursor_simm_lieux.execute(
            request_sql % (list_csv[x][0].replace("'", "''"), nom_dispositif.replace("'", "''"),
                           programme.replace("'", "''"),
                           critère_BEE.replace("'", "''"), indicateur_BEE.replace("'", "''"),
                           OE.replace("'", "''"), indicateurs_OE.replace("'", "''"),
                           parametres.replace("'", "''"),Bancarisation.replace("'", "''")))




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


data_list_a = csv_cleaner("CSV_file/import_colonies_fev2021.csv", "secteur_nom_fr", "longitude", "latitude", ";")
write_SQL(data_list_a)
conn_simm_lieux.commit();
conn_simm_lieux.close();