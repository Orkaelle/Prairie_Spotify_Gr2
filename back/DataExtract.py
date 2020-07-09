#récuper danceability, energy, tempo, id
from lxml import etree
import urllib.request
import json
import sqlite3
import os
import sys
import requests
import back.constants

"""
Connect to database
"""
#dbName = "bddSpotify_v2.db"
db_name = None
#base_dir = os.path.dirname(sys.argv[0])
dir_path = None
path = None
file_name = None
xml_path = None
bdd = None
cur = None
list_TOP50_URL = []
list_songs_URL = []

db_name = back.constants.DB_NAME
dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path, db_name)
file_name = back.constants.XML_SPOTIFY_NAME
xml_path = os.path.join(dir_path, file_name)

def connect_db():
    ## CONNEXION A LA BASE
    bdd = sqlite3.connect(path)
    
    return bdd

def get_xml_file():
    URL = "https://dlsandboxweu002.blob.core.windows.net/spotify?restype=container&comp=list"
    response = requests.get(URL)
    with open(xml_path, 'wb') as file:
        file.write(response.content)

def get_top50_url_list():
    tree = etree.parse(xml_path) 
    for url in tree.xpath("/EnumerationResults/Blobs/Blob/Url"):
        if "top_50" in url.text: 
            list_TOP50_URL.append(url.text) 
    print("Récupération URL TOP50 OK")

def get_urls_list():  
    tree = etree.parse(xml_path)
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

def extract_data():

    bdd = connect_db()
    cur=bdd.cursor()
    try:
        """
        get and save data from url
        """
        get_xml_file()

        """
        get only top 50 playlist
        """
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

                    #insert album
                    id_album = dic["items"][i]["track"]["album"]["id"]
                    name_album = dic["items"][i]["track"]["album"]["name"]
                    url_album = dic["items"][i]["track"]["album"]["images"][0]["url"]
                    donnees_album = [id_album, name_album, url_album]
                    cur.execute("""INSERT OR IGNORE INTO album(id_album, name_album, url_image) VALUES(?,?,?);""", donnees_album)

                    #insert titre
                    idTitre = dic["items"][i]["track"]["id"]
                    nameTitre = dic["items"][i]["track"]["name"]
                    durationTitre = dic["items"][i]["track"]["duration_ms"]
                    popularity = dic["items"][i]["track"]["popularity"]
                    donnees_titre=[idTitre, nameTitre, str(durationTitre), popularity]
                    cur.execute("""INSERT OR IGNORE INTO titre(id_titre, nom_titre, durée, popularity) VALUES(?,?,?,?);""", donnees_titre)

                    #insert album_titre
                    donnees_album_titre = [id_album, idTitre]
                    cur.execute("""INSERT OR IGNORE INTO album_titre(album_id, titre_id) VALUES(?,?);""", donnees_album_titre)

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
                    bpmenergintens = [str(dic["audio_features"][i]["tempo"]),str(dic["audio_features"][i]["energy"]),str(dic["audio_features"][i]["loudness"]),str(dic["audio_features"][i]["danceability"]),str(dic["audio_features"][i]["speechiness"]),str(dic["audio_features"][i]["liveness"]),str(dic["audio_features"][i]["valence"]),str(dic["audio_features"][i]["id"])]
                    cur.execute("""UPDATE titre SET bpm = ?, energie = ?, intensité = ?, danceability = ?, speechiness = ? , liveness = ? , valence = ? WHERE id_titre = ?""",bpmenergintens)

                    i += 1

        bdd.commit()
        return "Data extracted"
    except:
        return  "Extract data error: %s" % sys.exc_info()[0]
