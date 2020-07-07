import sqlite3
from bottle import route, run, debug, template, request, static_file, error
import back.OH_REQUETES as req

# only needed when you run Bottle on mod_wsgi
from bottle import default_app


@route('/nbr_artist')
def nombre_album_par_artist():

    result = req.get_nbr_chanson_par_artist()

    output = template('front/nbr_artist', rows=result)
    return output


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