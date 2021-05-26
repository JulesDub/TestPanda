import cx_Oracle
import psycopg2


#Connection à la base SIMM_LIEUX
conn_simm_lieux = psycopg2.connect(host='vpostgres10.ifremer.fr',database="simm_lieux",user='simm_lieux_user',password='',port= '5432')
cursor_simm_lieux = conn_simm_lieux.cursor();



#TODO Récupérer ces informations depuis la fiche 'dispositif'
#Nom dispositif
insert_dispositif="""Campagnes d’observation halieutique : évaluation des stocks"""
insert_pds="""Poissons céphalopodes/SP02 Poissons et Céphalopodes bentho-démersaux sur substrats meubles côtiers;Poissons céphalopodes/SP04 Poissons et Céphalopodes pélagiques et bentho-démersaux sur le plateau continental et au large;
Espèces commerciales/SP03 Echantillonnage des captures et paramètres biologiques;Espèces commerciales/SP04 Campagnes de surveillance halieutiqu"""
insert_critère_BEE="""D1C2 - Abondance des populations;D1C3 - Caractéristiques démographiques des populations;D1C4 - Distribution spatiale des populations;D1C5 - Habitat des espèces;D3C2 - Biomassse du stock reproducteur;D3C3 - Distribution des populations par âge/taille"""
### Ajouter indicateurs
insert_OE="""D01-PC-OE05;D03-OE02;D04-OE01;D04-OE02"""
### Ajouter indicateurs
insert_parametres = """ABU1-6 - Abondance (nombre);AGE1 - Distribution par âge;BIOM1-3 - Biomasse;DIST-P1 - Distribution (modèle);DIST-S1 - Distribution (spatiale);EXT1-13 - Étendue;INC2 - Occurrence;LEN1-3 - Longueur;
SEX-D1 - Distribution par sexe;SIZE-D1 - Distribution par taille;R-ABU3 - Abondance relative (calcul à court terme);R-ABU4 - Abondance relative (calcul à long terme);
R-ABU5 - Pourcentage de différence entre l’abondance de l’année de référence et celle de l'année la plus récente;TEND-ABU - Evolution de l'abondance"""
insert_bancarisation="""https://sih.ifremer.fr/Ecosystemes/Donnees-de-campagnes"""





# Connection à la base ORACLE des campagnes
# Ajouter module cx_Oracle ne suffit pas il faut installer l'instant client Oracle (https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html)
# Et ajouter le repertoire de l'instant client au path
#https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#installing-cx-oracle-on-windows

cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\instantclient_19_11")
dsn_tns = cx_Oracle.makedsn('insta-vip', '1521', service_name='INSTA_TAF') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect(user='SIS_READER', password='', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
c = conn.cursor()

# Fonction de récupération des données géographiques de chaque campagne
def insert_into_bdd_lieux(datarow):
    for row in datarow:
        cam_name = row[0]
        cam_zone = row[2]
        #TODO Vérifier si la trajectoire existe et mettre à jour les information
        if(cam_zone is not None):cam_zone=cam_zone.replace("'", "''")

        sql_find_traj = "select SDO_UTIL.TO_WKTGEOMETRY(traj.GEOMETRY) from cam INNER JOIN CAM_POLYLIGNE traj ON cam.cam_camref = traj.cam_camref where cam_crnom = :cam_name"
        c.execute(sql_find_traj,[cam_name])
        result = c.fetchone()
        if(result is not None):
            sql_find_traj = "select SDO_UTIL.TO_WKTGEOMETRY(traj.GEOMETRY) from cam INNER JOIN CAM_POLYLIGNE traj ON cam.cam_camref = traj.cam_camref where cam_crnom = :cam_name"
            c.execute(sql_find_traj, [cam_name])
            traj, = c.fetchone()
            print("With a trajectory")
            request_sql = """INSERT INTO LIEUX_SEXTANT    (LIEU_LIBELLE,
                	                                                LIEU_POSITION_TRAJECTOIRE,
                	                                                LIEU_DISPOSITIF,
                	                                                LIEU_PDS,
                	                                                LIEU_CRITERES_BEE,
                	                                                LIEU_OE,
                	                                                LIEU_PARAMETRES,
                	                                                LIEU_DCSMM_SRM,
                	                                                LIEU_BANCARISATION)
                	                    VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s')"""
            cursor_simm_lieux.execute(
                request_sql % (cam_name.replace("'", "''"), traj, insert_dispositif.replace("'", "''"),
                               insert_pds.replace("'", "''"),
                               insert_critère_BEE.replace("'", "''"), insert_OE.replace("'", "''"),
                               insert_parametres.replace("'", "''"), cam_zone,
                               insert_bancarisation.replace("'", "''")))

        else:
            print("Pas de trajectoires")


# TODO Essayer de récupérer les campagnes à partir de la fiche 'Dispositif'
campagne_list=['PELMED', 'MEDITS', 'PELGAS', 'ORHAGO','LANGOLF-TV','EVOHE','IBTS','CRUSTAFLAM','CGFS' ]

# Boucle pour chaque campagne
for campagne in campagne_list:
    #Récupération des information issues de la base campagne
    request ="SELECT CAM_CRNOM, CAM_CAMREF, CAM_ZONE from CAM WHERE CAM_CRNOM LIKE '%s%%'"
    c.execute(request % campagne)
    rows_campagnes_names = c.fetchall()
    insert_into_bdd_lieux(rows_campagnes_names)




## Manage commit and close connection
conn.close()
conn_simm_lieux.commit();
conn_simm_lieux.close();
