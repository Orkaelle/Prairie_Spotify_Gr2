########## !!! ATTENTION : NECESSITE D'AVOIR LANCER LE SCRIPT DE CREATION DE LA BASE AU MOINS UNE FOIS AVANT !!! ##########

## IMPORT DES LIBRAIRIES
import os
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import numpy as np



########################################### REQUETES ###########################################################
cur = None
bdd = None

def connect_db():
    ## CONNEXION A LA BASE
    path = os.path.dirname(sys.argv[0])
    bdd = sqlite3.connect(path + "/back/bddSpotify.db")
    
    return bdd

def get_nbr_chanson_par_artist():
    
    bdd = connect_db()
    cur = bdd.cursor()
    cur.execute('SELECT nom_artiste, COUNT(titre_id) FROM artiste INNER JOIN artiste_titre WHERE artiste.id_artiste = artiste_titre.artiste_id GROUP BY nom_artiste ORDER BY COUNT(titre_id) DESC')
    result = cur.fetchall()

    bdd.close()

    return result

def get_tps_moyen_des_morceaux():
    bdd = connect_db()
    cur = bdd.cursor()
    cur.execute('SELECT AVG(durée) FROM titre;')
    result_ms = cur.fetchall()

    result = round(result_ms[0][0]/60000,2)
    return result

def get_nbr_titres_par_bpm():
    bdd = connect_db()
    cur = bdd.cursor()
    cur.execute('SELECT COUNT(id_titre), CASE WHEN bpm < 60 THEN "Largo" WHEN bpm < 66 THEN "Larghetto" WHEN bpm < 76 THEN "Adagio" WHEN bpm < 108 THEN "Andante" WHEN bpm < 120 THEN "Moderato" WHEN bpm < 160 THEN "Allegro" WHEN bpm < 200 THEN "Presto" ELSE "Prestissimo" END AS bpm_intervalle FROM titre GROUP BY bpm_intervalle ')
    result = cur.fetchall()

    return result
    
def get_nbr_titres_multiplaylists():
    bdd = connect_db()
    cur = bdd.cursor()
    cur.execute('SELECT nom_titre, COUNT(playlist_id) FROM titre INNER JOIN playlist_titre WHERE titre.id_titre = playlist_titre.titre_id GROUP BY nom_titre HAVING COUNT(playlist_id) > 1;')
    result = cur.fetchall()

    return result

def get_relation_energie_intensite():
    bdd = connect_db()
    cur = bdd.cursor()   
    cur.execute('SELECT energie, intensité FROM titre;')
    rtRq5 = cur.fetchall()

    data = pd.DataFrame(rtRq5) # On convertit la liste rtRq5 générée précédemment en "DataFrame" pour l'exploiter en graphique par la suite

    # On convertit le DataFrame en matrices
    matrice = data.to_numpy()
    x, y = np.array_split(matrice, 2, axis=1)
    X = np.hstack((x, np.ones(x.shape)))
    theta = np.random.randn(2, 1)


    # Création du modèle
    def model(X, theta):
        return X.dot(theta)


    # Définition de la fonction de coût
    def cost_function(X, y, theta):
        m = len(y)
        return 1/(2*m) * np.sum((model(X, theta) - y)**2)


    def grad(X, y, theta):
        m = len(y)
        return 1/m * X.T.dot(model(X, theta) - y)


    def gradient_descent(X, y, theta, learning_rate, nb_iterations):
        for i in range(0, nb_iterations):
            theta = theta - learning_rate * grad(X, y, theta)
        return theta


    theta_final = gradient_descent(X, y, theta, learning_rate=1.25, nb_iterations=500)


    prediction = model(X, theta_final)


    def coef_determination(y, pred):
        u = ((y - pred)**2).sum()
        v = ((y - y.mean())**2).sum()
        return 1 - u/v

    plt.close()
    plt.scatter(x, y)
    plt.plot(x, prediction, c='r')
    plt.xlabel('Energie')
    plt.ylabel('Intensité')
    nom_image = "images/graph.png"
    plt.savefig(nom_image)
    plt.close()

    formule = "La droite a pour formule : " + str(round(theta[0][0],4)) + "x + " + str(round(theta[1][0],4)) + ". Le coefficient R² est de " + str(round(coef_determination(y, prediction),2)) + "."

    return formule
    


################################## FERMETURE DE LA BASE ###################################