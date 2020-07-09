"""
This file contains classes and functionalities that run xgboost algorithm
The prediction is based on song vs "songs in a playlist"
@author: Mathieu SIMON
@Date : 02/07/2020: creation of the class
"""

import os
import sys
from sklearn.metrics import roc_auc_score
import pandas as pd
import matplotlib
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
import copy
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

"""
SQL queries 
"""

SQL_GET_ALL_TRACKS_CHARACTERISTICS = """
        SELECT durée,
            bpm,
            energie,
            intensité,
            danceability,
            speechiness,
            liveness,
            valence,
            popularity,
            case when exists (select 1 
                                from playlist_titre 
                                inner join playlist on playlist_titre.playlist_id = '{}'  
                                where playlist_titre.titre_id = titre.id_titre ) 
                    then 1 
                    else 0 
                    end as isHit       
        FROM titre;
        """

SQL_GET_TRACK_CHARACTERISTICS = """
        SELECT durée,
            bpm,
            energie,
            intensité,
            danceability,
            speechiness,
            liveness,
            valence
        FROM titre
        WHERE nom_titre = '{}'"""

"""
The file path of database file
"""
path = os.path.dirname(sys.argv[0])


class XgBoost:
    """
    XgBoost toolset to predict the popularity of a song based on songs in a playlist
    """
    def __init__(self):
        """
        constructor
        """
        print("XgbBoost class is initiated")

  
       #Function to evaluate my model with Cross validation
    def testingModel(self, model, X_train, Y_train):
        """
        Train the model with input data
        """
        scores = cross_val_score(model, X_train, Y_train, cv=5, scoring = "roc_auc")
        print("Scores:", scores)
        print("Mean:", scores.mean())
        print("Standard Deviation:", scores.std())
        return scores.mean()

    def get_prediction(self, song, playlist):
        """
        Get prediction from trained model and dataset

        return min/max calculated prediction (isHit?)
        """
        conn = sqlite3.connect(path + "/back/bddSpotify.db")
        
        train = pd.read_sql_query(SQL_GET_ALL_TRACKS_CHARACTERISTICS.format(playlist), conn)

        Y = copy.deepcopy(train.isHit)
        Y.shape

        drop_list = ['isHit', 'popularity']
        train1 = train.drop(drop_list, axis=1)

        xgb1 = XGBClassifier(
        learning_rate =0.1,
        n_estimators=100,
        max_depth=5,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective= 'binary:logistic',
        nthread=4,
        scale_pos_weight=1,
        seed=27)
        xgb1.fit(train1, Y)
        self.testingModel(xgb1, train1, Y)

        track = pd.read_sql_query(SQL_GET_TRACK_CHARACTERISTICS.format(song), conn)

        if track.empty:
            raise Exception("song '{}' not found!".format(song))

        prediction = xgb1.predict_proba(track)

        print("Probabily of being a hit song : min {:.0f}% / max {:.0f}% ".format(prediction.min(), prediction.max()*100))

        return int(prediction.min()*100), int(prediction.max()*100)

        conn.close()



