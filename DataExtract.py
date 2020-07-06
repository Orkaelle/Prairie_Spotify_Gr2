#récuper danceability, energy, tempo, id
from lxml import etree
import urllib.request
import json
import sqlite3
import os
import sys

path = os.path.dirname(sys.argv[0])
bdd = sqlite3.connect(path + "/bddSpotify_v2.db")
cur=bdd.cursor()

list_TOP50_URL = []
list_songs_URL = []

def get_top50_url_list():
    tree = etree.parse(path + "/spotify_formated.xml") 
    for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
        if "top_50" in url.text: 
            list_TOP50_URL.append(url.text) 
    print("Récupération URL TOP50 OK")

def get_urls_list():  
    tree = etree.parse(path + "/spotify_formated.xml")
    for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
        if "songs" in url.text and "json" in url.text:
            list_songs_URL.append(url.text)

def read_json_file(url_link):
    webURL = urllib.request.urlopen(url_link)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    dic = json.loads(data.decode(encoding))

    return dic

def get_playlist_name(url_link):
    linkSplited = url_link.split("/")
    playlistName = linkSplited[len(linkSplited)-1].replace(".json", "")
    return playlistName

def get_playlist_id(playlist_href):
    linkSplited = playlist_href.split("/")
    playlisId = linkSplited[linkSplited.index("playlists") + 1]

    return playlisId

get_top50_url_list()

for top50 in list_TOP50_URL :
    
    dic = read_json_file(top50)

    i = 0
    j = 0

    if "error" in dic.keys() :
        print("lecture impossible")
    else :
        #get playlist id
        playlist_id = get_playlist_id(dic["href"])
        playlist_name = get_playlist_name(top50)
        donnees_playlist = [playlist_id, playlist_name]

        #insert into playlist
        cur.execute("""INSERT INTO playlist(id_playlist, nom_playlist) VALUES (?,?);""", donnees_playlist)

        while i < len(dic["items"]):

            top50_href = dic["href"]

            print("ligne ======> " + str(i))
            j = 0

            #insert titre
            idTitre = dic["items"][i]["track"]["id"]
            nameTitre = dic["items"][i]["track"]["name"]
            durationTitre = dic["items"][i]["track"]["duration_ms"]
            donnees_titre=[idTitre, nameTitre, str(durationTitre)]

            cur.execute("""INSERT OR IGNORE INTO titre(id_titre, nom_titre, durée) VALUES(?,?,?);""", donnees_titre)

            #insert playlist_titre
            donnees_playlist_titre = [playlist_id, idTitre]
            cur.execute("""INSERT INTO playlist_titre(playlist_id, titre_id) VALUES(?,?);""", donnees_playlist_titre)

            while j < len(dic["items"][i]["track"]["album"]["artists"]):

                #insert artist               
                idArtist = dic["items"][i]["track"]["album"]["artists"][j]["id"]
                nameArtist = dic["items"][i]["track"]["album"]["artists"][j]["name"]

                donnees_artist = [idArtist, nameArtist]
                cur.execute("""INSERT OR IGNORE INTO artiste(id_artiste, nom_artiste) VALUES(?,?);""", donnees_artist)

                #insert artist_titre
                donnees_artist_titre = [idTitre ,idArtist]
                cur.execute("""INSERT OR IGNORE INTO artiste_titre(titre_id, artiste_id) VALUES(?,?);""", donnees_artist_titre)

                j += 1

            i += 1

get_urls_list()

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
            cur.execute("""UPDATE titre SET bpm = ?, energie = ?, intensité = ? WHERE id_titre= ?""",bpmenergintens)

            i += 1

bdd.commit()