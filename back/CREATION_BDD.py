####################### CREATION DE LA BDD ET AJOUT DES DATAS #########################

## IMPORT DES LIBRAIRIES
import os
import sys
import sqlite3
import constants

## SUPPRESSION DE LA BDD EXISTANTE
## dbName = "bddSpotify_v2.db"
dbName = constants.DB_NAME
base_dir = os.path.dirname(sys.argv[0])
path = os.path.join(base_dir, dbName)

bdd = sqlite3.connect(path)
bdd.close()
os.remove(path)

## CREATION DE LA BDD
bdd = sqlite3.connect(path)
cur = bdd.cursor()


## CREATION TABLES
cur.execute('CREATE TABLE playlist(id_playlist PRIMARY KEY, nom_playlist TEXT);')
cur.execute('CREATE TABLE artiste(id_artiste TEXT PRIMARY KEY, nom_artiste TEXT);')
cur.execute('CREATE TABLE titre(id_titre TEXT PRIMARY KEY, nom_titre TEXT, durée REAL, bpm REAL, energie REAL, intensité REAL, danceability REAL, speechiness REAL, liveness REAL, valence REAL);')
cur.execute('CREATE TABLE album(id_album TEXT PRIMARY KEY, name_album TEXT, url_image TEXT);')
cur.execute('CREATE TABLE artiste_titre(titre_id TEXT, artiste_id TEXT, FOREIGN KEY (titre_id) REFERENCES titre(id_titre), FOREIGN KEY (artiste_id) REFERENCES artiste(id_artiste), PRIMARY KEY (titre_id, artiste_id));')
cur.execute('CREATE TABLE playlist_titre(playlist_id TEXT, titre_id TEXT, FOREIGN KEY (playlist_id) REFERENCES paylist(id_playlist), FOREIGN KEY (titre_id) REFERENCES titre(id_titre), PRIMARY KEY (playlist_id, titre_id));')
cur.execute('CREATE TABLE album_titre(album_id, titre_id TEXT, FOREIGN KEY (titre_id) REFERENCES titre(id_titre), FOREIGN KEY (album_id) REFERENCES album(id_album), PRIMARY KEY (titre_id, album_id));')
print("Création des tables effectuée.")


## SAUVEGARDE DE LA BDD
bdd.commit()
print("BDD sauvegardée.")


## FERMETURE BDD
bdd.close()
