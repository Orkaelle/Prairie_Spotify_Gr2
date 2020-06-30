########## !!! ATTENTION : NECESSITE D'AVOIR LANCER LE SCRIPT DE CREATION DE LA BASE AU MOINS UNE FOIS AVANT !!! ##########

## IMPORT DES LIBRAIRIES
import os, sys, sqlite3

## CONNEXION A LA BASE
path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify.db")
cur = bdd.cursor()

## REQUETES
# Nombre de titres par artiste :
cur.execute('SELECT nom_artiste, COUNT(titre_id) FROM artiste INNER JOIN artiste_titre WHERE artiste.id_artiste = artiste_titre.artiste_id GROUP BY nom_artiste')
rtRq1 = cur.fetchall()
print ("Nombre de titres par artiste :")
for i in rtRq1 :
    print (i)
# Temps moyen des morceaux :
cur.execute('SELECT AVG(durée) FROM titre;')
rtRq2 = cur.fetchall()
print ("Le temps moyen des morceaux est de " +str(rtRq2))
# Nombre de morceaux qui sont dans plusieurs playlists
cur.execute('SELECT nom_titre, COUNT(playlist_id) FROM titre INNER JOIN playlist_titre WHERE titre.id_titre = playlist_titre.titre_id GROUP BY nom_titre HAVING COUNT(playlist_id) > 1;')
rtRq3 = cur.fetchall()
print (str(len(rtRq3)) + " titres sont dans plusieurs playlists.")
# Nombre de morceaux par bpm
cur.execute('SELECT COUNT(id_titre), CASE WHEN bpm < 60 THEN "Largo" WHEN bpm < 66 THEN "Larghetto" WHEN bpm < 76 THEN "Adagio" WHEN bpm < 108 THEN "Andante" WHEN bpm < 120 THEN "Moderato" WHEN bpm < 160 THEN "Allegro" WHEN bpm < 200 THEN "Presto" ELSE "Prestissimo" END AS bpm_intervalle FROM titre GROUP BY bpm_intervalle ')
rtRq4 = cur.fetchall()
print ("Nombre de morceaux par intervalle de bpm :")
for i in rtRq4 :
    print (i)

## FERMETURE DE LA BASE
bdd.close