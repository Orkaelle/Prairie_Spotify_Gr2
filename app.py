from bottle import Bottle, run, \
     template, debug, static_file

import os, sys
import back.OH_REQUETES as req

dirname = os.path.dirname(sys.argv[0])

app = Bottle()
debug(True)

@app.route('/static/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root=dirname+'/static/asset/css')

@app.route('/static/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root=dirname+'/static/asset/js')

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

    output = template('energie_intensite', chemin = result)


"""
Run server
"""
run(app, host='localhost', port = 8080)
