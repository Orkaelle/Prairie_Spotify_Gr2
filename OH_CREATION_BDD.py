####################### CREATION DE LA BDD ET AJOUT DES DATAS #########################

## IMPORT DES LIBRAIRIES
import os, sys, sqlite3

## SUPPRESSION DE LA BDD EXISTANTE
path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify.db")
bdd.close()
os.remove(path + "/bddSpotify.db")

## CREATION DE LA BDD
bdd = sqlite3.connect(path + "/bddSpotify.db")
cur = bdd.cursor()


## CREATION TABLES
cur.execute('CREATE TABLE artiste (id_artiste INTEGER PRIMARY KEY AUTOINCREMENT, nom_artiste TEXT UNIQUE);')
cur.execute('CREATE TABLE titre (id_titre INTEGER PRIMARY KEY AUTOINCREMENT, nom_titre TEXT UNIQUE, durée REAL, bpm REAL, energie REAL, intensité REAL, id_spotify text);')
cur.execute('CREATE TABLE playlist (id_playlist INTEGER PRIMARY KEY AUTOINCREMENT, nom_playlist TEXT);')
cur.execute('CREATE TABLE artiste_titre (titre_id INTEGER, artiste_id INTEGER, FOREIGN KEY (titre_id) REFERENCES titre(id_titre), FOREIGN KEY (artiste_id) REFERENCES artiste(id_artiste), PRIMARY KEY (titre_id, artiste_id));')
cur.execute('CREATE TABLE playlist_titre (playlist_id INTEGER, titre_id INTEGER, FOREIGN KEY (playlist_id) REFERENCES paylist(id_playlist), FOREIGN KEY (titre_id) REFERENCES titre(id_titre), PRIMARY KEY (playlist_id, titre_id));')
print("Création des tables effectuée.")


## SAUVEGARDE DE LA BDD
bdd.commit()
print("BDD sauvegardée.")


## FERMETURE BDD
bdd.close()
