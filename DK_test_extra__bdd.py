#récuper danceability, energy, tempo, id
from lxml import etree
import urllib.request
import json
import sqlite3
import os
import sys


path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify.db")
cur=bdd.cursor()

list_TOP50_URL = []
tree = etree.parse(path + "/spotify_formated.xml")
for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
    if "top_50" in url.text: 
        list_TOP50_URL.append(url.text) 
print("Récupération URL TOP50 OK")

for top50 in list_TOP50_URL :
    webURL = urllib.request.urlopen(top50)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))
    i = 0
    j = 0

    #get playlist name
    linkSplited = top50.split("/")
    playlistName = linkSplited[len(linkSplited)-1].replace(".json", "")

    #insert into playlist
    sqlStr = "INSERT OR IGNORE INTO playlist (nom_playlist) VALUES('" + playlistName + "')"
    cur.execute(sqlStr)
    idPlaylist = cur.lastrowid

    if idPlaylist == 0:
        sqlStr = "SELECT id_playlist from playlist where nom_playlist = '" + playlistName + "'"
        idPlaylist = cur.execute(sqlStr).fetchone()[0]


    if "error" in dic.keys() :
        print("lecture impossible")
    else :
        while i < len(dic["items"]):
            print("ligne ======> " + str(i))
            j = 0
            list_artist = []
            idArtist = 0
            idTitre = 0

            #get artits
            while j < len(dic["items"][i]["track"]["artists"]):

                nom_artiste = [str(dic["items"][i]["track"]["artists"][j]["name"])]

                idArtist = cur.execute("""SELECT id_artiste from artiste where nom_artiste = ?;""", nom_artiste).fetchone()[0]
                
                cur.execute("""INSERT OR IGNORE INTO artiste (nom_artiste) VALUES(?);""", nom_artiste)
                idArtist = cur.lastrowid
                
                #ajouter l'id artist à la list d'artistes
                list_artist.append(idArtist)
                
                j += 1

            #insert into titre
            données_titre=[str(dic["items"][i]["track"]["name"]),str(dic["items"][i]["track"]["duration_ms"]),dic["items"][i]["track"]["id"]]
            cur.execute("""INSERT OR IGNORE INTO titre(nom_titre,durée,id_spotify) VALUES(?,?,?);""",données_titre)
            idTitre = cur.lastrowid

            if idTitre == 0:
                sqlStr = "SELECT id_titre from titre where nom_titre = '" + dic["items"][i]["track"]["name"] + "'"
                idTitre = cur.execute(sqlStr).fetchone()[0]

            #insert into titre_artist
            for artist in list_artist:

                sqlStr = "INSERT OR IGNORE INTO artiste_titre(titre_id, artiste_id) VALUES(" + str(idTitre) + ", " + str(artist) + ")"
                cur.execute(sqlStr)

            #insert into titre_playlist
            sqlStr = "INSERT OR IGNORE INTO playlist_titre(playlist_id, titre_id) VALUES(" + str(idPlaylist) + ", " + str(idTitre) + ")"
            cur.execute(sqlStr)
                         
            i += 1
    break
    
'''
list_songs_URL = []
tree = etree.parse(path + "/spotify_formated.xml")
for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
    if "songs" in url.text and "json" in url.text:
         list_songs_URL.append(url.text)
        

for songs in list_songs_URL :
    webURL2 = urllib.request.urlopen(songs)    
    data = webURL2.read()
    encoding = webURL2.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))
    i = 0
    j = 0
    if "error" in dic.keys() :
        print("lecture impossible")
    else :
        while i < len(dic["audio_features"]):
            bpmenergintens = [str(dic["audio_features"][i]["tempo"]),str(dic["audio_features"][i]["energy"]),str(dic["audio_features"][i]["loudness"]),str(dic["audio_features"][i]["id"])]
            cur.execute("""UPDATE titre SET bpm = ?, energie = ?, intensité = ? WHERE id_spotify= ?""",bpmenergintens)

            i += 1
'''
bdd.commit()