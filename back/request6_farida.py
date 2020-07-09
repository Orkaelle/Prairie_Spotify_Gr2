import sqlite3
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import numpy

# se connecter à la base de données
path = os.path.dirname(sys.argv[0])
conn = sqlite3.connect(path + "/back/bddSpotify.db")

IMAGE_PATH = os.getcwd() + os.sep + "images" +  os.sep 

def compute_prediction() :
    graphs = []

    # transformation de jeu de données en Data Frame de pandas
    query = 'SELECT nom_titre, durée, energie, danceability, speechiness, liveness, valence, popularity FROM titre'
    df = pandas.read_sql(sql = query, con = conn)
    #print(df.columns)
    print("Data frame:", df)
    #
    columns = df.columns.tolist()
    columns = [c for c in columns if c not in ["nom_titre"]]
    print(df.shape)

    plt.close()
    # histogramme de la colonne danceability
    plt.hist(df["danceability"])
    #afficher le graphe
    plt.title("danceability")
    plt.savefig(IMAGE_PATH + "danceability")
    plt.close()
    graphs.append("danceability")

    # histogramme de la colonne speechiness
    plt.hist(df["speechiness"])
    #afficher le graphe
    plt.title("speechiness")
    plt.savefig(IMAGE_PATH + "speechiness")
    plt.close()
    graphs.append("speechiness")

    # histogramme de la colonne liveness
    plt.hist(df["liveness"])
    #afficher le graphe
    plt.title("liveness")
    plt.savefig(IMAGE_PATH + "liveness")
    plt.close()
    graphs.append("liveness")

    # histogramme de la colonne valence
    plt.hist(df["valence"])
    #afficher le graphe
    plt.title("valence")
    plt.savefig(IMAGE_PATH + "valence")
    plt.close()
    graphs.append("valence")

    # histogramme de la colonne energie
    plt.hist(df["energie"])
    #afficher le graphe
    plt.title("energie")
    plt.savefig(IMAGE_PATH + "energie")
    plt.close()
    graphs.append("energie")

    # histogramme de la colonne popularity
    plt.hist(df["popularity"])
    #afficher le graphe
    plt.title("popularity")
    plt.savefig(IMAGE_PATH + "popularity")
    plt.close()
    graphs.append("popularity")

    # création d'une matrice de correlation
    matrice_corr = df.corr().round(1)
    sns.heatmap(data = matrice_corr, annot=True)

    #stocker la variable à prédire

    target = "popularity"

    # générer l'ensemble d'apprentissage, définir un état aléatoire pour reproduire les résultats
    train = df.sample(frac=0.8, random_state=5)

    # selectionner qqc qui n'est pas dans l'apprentissage
    test = df.loc[~df.index.isin(train.index)]

    # afficher les graphes des deux états 
    print("Training set shape:", train.shape)
    print("Testing set shape:", test.shape)

    # Initialiser la classe du modèle
    lin_model = LinearRegression()
    # Fit the model to the training data.
    lin_model.fit(train[columns], train[target])

    # générer les predictions
    lin_predictions = lin_model.predict(test[columns])
    print("Predictions:", lin_predictions)
    # calcul d'erreur entre les prédictions et les valeurs fournies
    lin_mse = mean_squared_error(lin_predictions, test[target])
    print("Computed error:", lin_mse)

    return graphs, lin_predictions, lin_mse
