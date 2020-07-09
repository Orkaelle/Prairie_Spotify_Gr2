import os
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

"""
SQL queries 
"""
GET_ALBUMS = """SELECT name_album,
                url_image,
                CASE WHEN url_image = '{}' THEN 1 ELSE 0 END as selected
                FROM album
                 ORDER BY name_album ASC"""

SQL_GET_PLAYLISTS = """SELECT id_playlist,
                        nom_playlist,
                        CASE WHEN id_playlist = '{}' THEN 1 ELSE 0 END as selected
                        FROM playlist;
                    """




def get_albums(cover):
    """Get list of albums
    """
    ## CONNEXION A LA BASE
    path = os.path.dirname(sys.argv[0])
    bdd = sqlite3.connect(path + "/back/bddSpotify.db")
    cur = bdd.cursor()

    cur.execute(GET_ALBUMS.format(cover))
    result = cur.fetchall()

    return result

def get_playlists(selected):
    """
    Get the content of PLAYLIST table
    Return dictionnary
    """
    path = os.path.dirname(sys.argv[0])
    bdd = sqlite3.connect(path + "/back/bddSpotify.db")
    cur = bdd.cursor()

    cur.execute(SQL_GET_PLAYLISTS.format(selected))
    result = cur.fetchall()
    return result
