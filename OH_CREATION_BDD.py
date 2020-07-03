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
cur.execute('CREATE TABLE titre (id_titre INTEGER PRIMARY KEY AUTOINCREMENT, nom_titre TEXT UNIQUE, durée REAL, bpm REAL, energie REAL, intensité REAL, danceability REAL, speechiness REAL, liveness REAL, valence REAL, id_spotify text);')
cur.execute('CREATE TABLE playlist (id_playlist INTEGER PRIMARY KEY AUTOINCREMENT, nom_playlist TEXT);')
cur.execute('CREATE TABLE artiste_titre (titre_id INTEGER, artiste_id INTEGER, FOREIGN KEY (titre_id) REFERENCES titre(id_titre), FOREIGN KEY (artiste_id) REFERENCES artiste(id_artiste), PRIMARY KEY (titre_id, artiste_id));')
cur.execute('CREATE TABLE playlist_titre (playlist_id INTEGER, titre_id INTEGER, FOREIGN KEY (playlist_id) REFERENCES paylist(id_playlist), FOREIGN KEY (titre_id) REFERENCES titre(id_titre), PRIMARY KEY (playlist_id, titre_id));')
print("Création des tables effectuée.")


<<<<<<< Updated upstream
## SAUVEGARDE DE LA BDD
bdd.commit()
print("BDD sauvegardée.")
=======
bdd.commit()

# REQUETE
# Nombre de titres par artiste :
cur.execute('SELECT nom_artiste, COUNT(titre_id) FROM artiste INNER JOIN artiste_titre WHERE artiste.id_artiste = artiste_titre.artiste_id GROUP BY nom_artiste')
view = cur.fetchall()
for i in view :
    print(i)
# Temps moyen des morceaux :
cur.execute('SELECT AVG(durée) FROM titre;')
view = cur.fetchall()
for i in view :
    print ("Le temps moyen des morceaux est de " +str(i))
# Nombre de morceaux qui sont dans plusieurs playlists
cur.execute('SELECT nom_titre, COUNT(playlist_id) FROM titre INNER JOIN playlist_titre WHERE titre.id_titre = playlist_titre.titre_id GROUP BY nom_titre')
view = cur.fetchall()
for i in view :
    print (i)
    # if 

# # AFFICHAGE RESULTAT
# view = cur.fetchall()
# for i in view :
#     print (i)
>>>>>>> Stashed changes


## FERMETURE BDD
bdd.close()
