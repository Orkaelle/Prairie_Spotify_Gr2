import json
import os, sys
from bottle import Bottle, run, request, template, debug, static_file

import os
import sys
import back.OH_REQUETES as req
import back.DataExtract as data_extract
import back.CREATION_BDD as db
import sqlite3
import back.constants
from yolo.yolo import *
from back.bdd_requests import * 

dirname = os.path.dirname(sys.argv[0])

app = Bottle()

debug(True)

@app.route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/asset/css')

@app.route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dirname+'/static/asset/js')

@app.route('/images/<filename:re:.*\.png>')
def images(filename):
    return static_file(filename, root=dirname+'/images')

"""

"""
@app.route('/')
def index():
    data = {"developer_name":"Power Rangers",
            "developer_organization":"Simplon"}
    return template('index', data = data)

"""
Nombre de chansons par artiste
"""
@app.route('/nbr_artist')
def nombre_album_par_artist():

    result = req.get_nbr_chanson_par_artist()

    output = template('nbr_artist', rows=result)
    return output

"""
Durée moyenne des morceaux
"""
@app.route('/tps_moyen_morceaux')
def tps_moyen_morceaux():

    result = req.get_tps_moyen_des_morceaux()

    output = template('tps_moyen_morceaux', tps=result)
    return output

"""
Nombre de morceaux par bpm
"""
@app.route('/bpm')
def nombre_titres_par_bpm():

    result = req.get_nbr_titres_par_bpm()

    output = template('bpm', rows = result)
    return output

"""
Nombre de morceaux qui sont dans plusieurs playlists
"""
@app.route('/multiplaylists')
def nombre_de_titres_multiplaylists():

    result = req.get_nbr_titres_multiplaylists()
    nbtitres = len(result)

    output = template('multiplaylists', count = nbtitres, rows = result)
    return output


"""
Analyser et afficher la relation entre l’énergie et l’intensité
"""
@app.route('/energie_intensite')
def relation_energie_intensite():

    result = req.get_relation_energie_intensite()

    output = template('energie_intensite', resultat = result)
    return output

@app.get('/load_data')
def load_data():
    
    db_creation = db.create_database()
    extract = data_extract.extract_data()
    message = "%s and %s" % (db_creation, extract)
    
    return template('index', data = message)
#local resources
@app.route('/path/to/cover')
def serve_pictures():
    if not os.path.exists(TEMPORARY_FILE_OUT):
        return
    filename = os.path.basename(TEMPORARY_FILE_OUT)
    return static_file(filename, root=TEMPORARY_FILE_OUT.replace(filename,''))

@app.route('/cover', method='GET')
def cover_descriptor():
    cleanup_files()
    cover =  request.query.album_cover
    albums = get_albums(cover)
    identifications = []
    if cover != '' :
        identifications = cover_analysis(cover)

    return template("cover_ia", albums=albums, identifications=identifications, toto = cover)



"""
Run server
"""
run(app, host='localhost', port = 8080)
