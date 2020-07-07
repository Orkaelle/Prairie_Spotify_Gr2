import sqlite3
from bottle import route, run, debug, template, request, static_file, error
import back.OH_REQUETES as req

# only needed when you run Bottle on mod_wsgi
from bottle import default_app


@route('/nbr_artist')
def nombre_album_par_artist():

    result = req.get_nbr_chanson_par_artist()

    output = template('front/nbr_artist', rows = result)
    return output


@route('/bpm')
def nombre_titres_par_bpm():

    result = req.get_nbr_titres_par_bpm()

    output = template('front/bpm', rows = result)
    return output


@route('/multiplaylists')
def nombre_de_titres_multiplaylists():

    result = req.get_nbr_titres_multiplaylists()
    nbtitres = len(result)

    output = template('front/multiplaylists', count = nbtitres, rows = result)
    return output


@route('/energie_intensite')
def relation_energie_intensite():

    result = req.get_relation_energie_intensite()

    output = template('front/energie_intensite', chemin = result)


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(reloader=True)
# remember to remove reloader=True and debug(True) when you move your
# application from development to a productive environment